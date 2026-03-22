# This file is part of CycloneDX Python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

from argparse import OPTIONAL, ArgumentParser
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from os.path import basename, dirname, isfile, join
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Optional

from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.dependency import Dependency
from packageurl import PackageURL
from packaging.markers import Marker, default_environment
from packaging.requirements import Requirement

from . import BomBuilder, PropertyName, PurlTypePypi
from .cli_common import add_argument_mc_type
from .utils.cdx import make_bom
from .utils.packaging import normalize_packagename
from .utils.pyproject import pyproject2component
from .utils.secret import redact_auth_from_url
from .utils.toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import ComponentType

    T_NameDict = dict[str, Any]


class ExtrasNotFoundError(ValueError):
    def __init__(self, extras: Iterable[str]) -> None:
        self.__extras = frozenset(extras)

    def __str__(self) -> str:
        return f'Extra(s) [{",".join(sorted(self.__extras))}] not specified.'


class GroupsNotFoundError(ValueError):
    def __init__(self, groups: Iterable[str]) -> None:
        self.__groups = frozenset(groups)

    def __str__(self) -> str:
        return 'Group(s) not found: ' + ', '.join(sorted(self.__groups))


@dataclass
class _LockEntry:
    name: str
    component: Component
    dependencies: frozenset[str]  # keys MUST go through `normalize_packagename()`
    added2bom: bool


class UvBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(
            description=dedent("""\
                Build an SBOM from uv project.

                This requires parsing your `pyproject.toml` and `uv.lock` file which details exact pinned versions of
                dependencies.
                """),
            **kwargs)
        p.add_argument('--group',
                       metavar='<group>',
                       help='Include dependencies from the specified dependency group'
                            ' (multiple values allowed)',
                       action='append',
                       dest='groups_with',
                       default=[])
        p.add_argument('--no-group',
                       metavar='<group>',
                       help='Exclude dependencies from the specified dependency group'
                            ' (multiple values allowed)',
                       action='append',
                       dest='groups_without',
                       default=[])
        og = p.add_mutually_exclusive_group()
        og.add_argument('--only-group',
                        metavar='<group>',
                        help='Only include dependencies from the specified dependency group'
                             ' (multiple values allowed)',
                        action='append',
                        dest='groups_only',
                        default=[])
        og.add_argument('--only-dev',
                        help='Alias for: --only-group dev',
                        dest='only_dev',
                        action='store_true')
        del og
        p.add_argument('--all-groups',
                       help='Include all dependency groups'
                            ' (default: %(default)s)',
                       dest='all_groups',
                       action='store_true',
                       default=False)
        p.add_argument('--no-default-groups',
                       help='Ignore the default dependency groups'
                            ' (default: %(default)s)',
                       dest='no_default_groups',
                       action='store_true',
                       default=False)
        p.add_argument('--no-dev',
                       help='Alias for: --no-group dev',
                       dest='no_dev',
                       action='store_true',
                       default=False)
        eg = p.add_mutually_exclusive_group()
        eg.add_argument('-E', '--extras',
                        metavar='<extras>',
                        help='Extra sets of dependencies to include'
                             ' (multiple values allowed)',
                        action='append',
                        dest='extras',
                        default=[])
        eg.add_argument('--all-extras',
                        help='Include all extra dependencies'
                             ' (default: %(default)s)',
                        action='store_true',
                        dest='all_extras',
                        default=False)
        del eg
        add_argument_mc_type(p)
        p.add_argument('project_directory',
                       metavar='<project-directory>',
                       help='The project directory for uv (containing `pyproject.toml` and `uv.lock`),'
                            ' or a path to `uv.lock`'
                            ' (default: current working directory)',
                       nargs=OPTIONAL,
                       default='.')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **__: Any) -> None:
        self._logger = logger
        self.__marker_env_base: dict[str, str] = {}
        self.__marker_env_by_extra: dict[str, dict[str, str]] = {}
        self.__active_resolution_markers: Optional[frozenset[str]] = None

    def __marker_env(self, *, extra: Optional[str]) -> dict[str, str]:
        extra_n = normalize_packagename(extra) if extra else ''
        cached = self.__marker_env_by_extra.get(extra_n)
        if cached is not None:
            return cached
        env = dict(self.__marker_env_base)
        env['extra'] = extra_n
        self.__marker_env_by_extra[extra_n] = env
        return env

    def __is_marker_ok(self, marker: Any, *, extra: Optional[str] = None) -> bool:
        if not marker:
            return True
        try:
            marker_s = str(marker)
            return Marker(marker_s).evaluate(self.__marker_env(extra=extra))
        except Exception as err:  # pragma: no cover
            self._logger.debug('failed evaluating marker %r', marker, exc_info=err)
            return True

    def __select_active_resolution_markers(self, locker: 'T_NameDict') -> Optional[frozenset[str]]:
        markers = locker.get('resolution-markers')
        if not isinstance(markers, list) or len(markers) == 0:
            return None
        active = frozenset(str(m) for m in markers if self.__is_marker_ok(m))
        if len(active) == 0:
            raise ValueError('uv lock has resolution-markers but none match the current environment')
        if len(active) > 1:
            self._logger.warning('uv lock has multiple matching resolution-markers: %s', ', '.join(sorted(active)))
        return active

    def __call__(self, *,  # type:ignore[override]
                 project_directory: str,
                 groups_with: list[str],
                 groups_without: list[str],
                 groups_only: list[str],
                 only_dev: bool,
                 all_groups: bool,
                 no_default_groups: bool,
                 no_dev: bool,
                 extras: list[str],
                 all_extras: bool,
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        if isfile(project_directory) and basename(project_directory) == 'uv.lock':
            lock_file = project_directory
            project_directory = dirname(project_directory) or '.'
            pyproject_file = join(project_directory, 'pyproject.toml')
        else:
            pyproject_file = join(project_directory, 'pyproject.toml')
            lock_file = join(project_directory, 'uv.lock')
        try:
            pyproject_fh = open(pyproject_file, encoding='utf8', errors='replace')
        except OSError as err:
            raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
        try:
            lock_fh = open(lock_file, encoding='utf8', errors='replace')
        except OSError as err:
            pyproject_fh.close()
            raise ValueError(f'Could not open lock file: {lock_file}') from err

        with pyproject_fh, lock_fh:
            pyproject: 'T_NameDict' = toml_loads(pyproject_fh.read())
            locker: 'T_NameDict' = toml_loads(lock_fh.read())
            self.__marker_env_base = default_environment()
            self.__marker_env_by_extra.clear()
            self.__active_resolution_markers = self.__select_active_resolution_markers(locker)

            root_c = pyproject2component(pyproject,
                                         ctype=mc_type,
                                         fpath=pyproject_file,
                                         gather_license_texts=False,
                                         logger=self._logger)
            root_c.bom_ref.value = 'root-component'

            groups_available = self.__get_dependency_groups(pyproject, locker)
            groups_with_s = frozenset(map(normalize_packagename,
                                          filter(None, ','.join(groups_with).split(','))))
            groups_without_s = frozenset(map(normalize_packagename,
                                             filter(None, ','.join(groups_without).split(','))))
            groups_only_s = frozenset(map(normalize_packagename,
                                          filter(None, ','.join(groups_only).split(','))))
            del groups_with, groups_without, groups_only

            if only_dev:
                groups_only_s = frozenset({'dev', })
            if no_dev:
                groups_without_s = groups_without_s | frozenset({'dev', })
            if only_dev and no_dev:
                raise ValueError('`--only-dev` and `--no-dev` are mutually exclusive')

            all_groups_s = frozenset(groups_available)
            groups_requested = groups_with_s | groups_without_s | groups_only_s
            groups_unknown = groups_requested - all_groups_s
            if len(groups_unknown) > 0:
                groups_error = GroupsNotFoundError(groups_unknown)
                self._logger.error(groups_error)
                raise ValueError('some uv dependency groups are unknown') from groups_error

            include_project_deps = len(groups_only_s) == 0
            use_groups: frozenset[str]
            if groups_only_s:
                use_groups = groups_only_s - groups_without_s
            else:
                use_groups = set()
                if all_groups:
                    use_groups.update(all_groups_s)
                else:
                    if not no_default_groups:
                        use_groups.update(self.__get_default_groups(pyproject, all_groups_s))
                    use_groups.update(groups_with_s)
                use_groups = frozenset(use_groups - groups_without_s)
            del groups_with_s, groups_without_s, groups_only_s, groups_requested, groups_unknown

            extras_s: frozenset[str]
            if include_project_deps:
                if all_extras:
                    extras_s = frozenset(self.__get_optional_dependencies(pyproject, locker))
                else:
                    extras_s = frozenset(map(normalize_packagename,
                                             filter(None, ','.join(extras).split(','))))

                optional_deps = self.__get_optional_dependencies(pyproject, locker)
                extras_not_found = extras_s - optional_deps.keys()
                if len(extras_not_found) > 0:
                    extras_error = ExtrasNotFoundError(extras_not_found)
                    self._logger.error(extras_error)
                    raise ValueError('some package extras are unknown') from extras_error
                del extras_not_found
            else:
                # `--only-group` / `--only-dev` implies no project selection, so extras are ignored.
                extras_s = frozenset()

            return self._make_bom(
                root_c,
                locker,
                self.__get_dependency_seeds(pyproject, locker, extras_s, use_groups, include_project_deps),
                extras_s,
            )

    def __get_dependency_seeds(self, pyproject: 'T_NameDict', locker: 'T_NameDict',
                               extras: frozenset[str],
                               groups: frozenset[str],
                               include_project_deps: bool
                               ) -> tuple[frozenset[str], dict[str, frozenset[str]]]:
        """
        Determine which packages are included, based on `pyproject.toml` manifest.

        This mimics how `uv sync` behaves by default: base dependencies, dependencies from the default group set,
        plus selected extras.
        """
        dep_names: set[str] = set()
        required_extras: dict[str, set[str]] = {}

        def add_req(req: Requirement, *, marker_extra: Optional[str]) -> None:
            if req.marker is not None:
                try:
                    if not req.marker.evaluate(self.__marker_env(extra=marker_extra)):
                        return
                except Exception as err:  # pragma: no cover
                    self._logger.debug('failed evaluating marker %r', req.marker, exc_info=err)
            name = normalize_packagename(req.name)
            dep_names.add(name)
            if req.extras:
                required_extras.setdefault(name, set()).update(map(normalize_packagename, req.extras))

        project = pyproject.get('project')
        if include_project_deps:
            if isinstance(project, dict):
                for dep in project.get('dependencies', ()):
                    try:
                        add_req(Requirement(dep), marker_extra=None)
                    except Exception as err:  # pragma: no cover
                        self._logger.debug('failed parsing dependency %r', dep, exc_info=err)

                raw_optional = project.get('optional-dependencies', {})
                if isinstance(raw_optional, dict):
                    for extra_raw, dep_specs in raw_optional.items():
                        extra = normalize_packagename(str(extra_raw))
                        if extra not in extras:
                            continue
                        for dep_spec in dep_specs or ():
                            try:
                                add_req(Requirement(dep_spec), marker_extra=extra)
                            except Exception as err:  # pragma: no cover
                                self._logger.debug('failed parsing optional dependency %r', dep_spec, exc_info=err)
            else:
                # best-effort fallback: rely on lockfile-only metadata
                lock_root = self.__get_lock_root(locker, root_name=None)
                if lock_root is not None:
                    dep_names.update(lock_root.dependencies)
                    optional_deps = self.__optional_dependencies_from_lock(lock_root.package)
                    for extra in extras:
                        dep_names.update(optional_deps.get(extra, ()))

        if groups:
            for group in groups:
                for dep_name, dep_extras in self.__group_dependencies(pyproject, locker, group).items():
                    dep_names.add(dep_name)
                    if dep_extras:
                        required_extras.setdefault(dep_name, set()).update(dep_extras)
                for dep_spec in self.__group_dependency_specs(pyproject, group):
                    try:
                        add_req(Requirement(dep_spec), marker_extra=None)
                    except Exception as err:  # pragma: no cover
                        self._logger.debug('failed parsing group dependency %r', dep_spec, exc_info=err)

        return frozenset(dep_names), {k: frozenset(v) for k, v in required_extras.items()}

    def __get_optional_dependencies(self, pyproject: 'T_NameDict', locker: 'T_NameDict') -> dict[str, frozenset[str]]:
        project = pyproject.get('project')
        if isinstance(project, dict):
            raw = project.get('optional-dependencies', {})
            if isinstance(raw, dict):
                deps: dict[str, set[str]] = {}
                for extra_raw, dep_specs in raw.items():
                    extra = normalize_packagename(str(extra_raw))
                    deps.setdefault(extra, set())
                    for dep_spec in dep_specs or ():
                        try:
                            req = Requirement(dep_spec)
                        except Exception as err:  # pragma: no cover
                            self._logger.debug('failed parsing optional dependency %r', dep_spec, exc_info=err)
                            continue
                        deps[extra].add(normalize_packagename(req.name))
                return {k: frozenset(v) for k, v in deps.items()}

        # best-effort fallback: lockfile may still contain this info
        lock_root = self.__get_lock_root(locker, root_name=None)
        if lock_root is None:
            return {}
        return {k: frozenset(v) for k, v in self.__optional_dependencies_from_lock(lock_root.package).items()}

    def __get_dependency_groups(self, pyproject: 'T_NameDict', locker: 'T_NameDict') -> dict[str, frozenset[str]]:
        """
        Determine which dependency groups are available.

        Groups are primarily sourced from PEP 735 `dependency-groups` and uv's legacy `tool.uv.dev-dependencies`.
        As a fallback, groups are also discovered from `uv.lock`.
        """
        groups: dict[str, set[str]] = {}

        raw = pyproject.get('dependency-groups', {})
        if isinstance(raw, dict):
            for group_raw, dep_specs in raw.items():
                group = normalize_packagename(str(group_raw))
                groups.setdefault(group, set())
                for dep_spec in dep_specs or ():
                    try:
                        req = Requirement(str(dep_spec))
                    except Exception as err:  # pragma: no cover
                        self._logger.debug('failed parsing dependency group requirement %r', dep_spec, exc_info=err)
                        continue
                    groups[group].add(normalize_packagename(req.name))

        tool = pyproject.get('tool', {})
        if isinstance(tool, dict):
            tool_uv = tool.get('uv', {})
            if isinstance(tool_uv, dict):
                legacy_dev = tool_uv.get('dev-dependencies', ())
                if isinstance(legacy_dev, list):
                    groups.setdefault('dev', set())
                    for dep_spec in legacy_dev or ():
                        try:
                            req = Requirement(str(dep_spec))
                        except Exception as err:  # pragma: no cover
                            self._logger.debug('failed parsing legacy dev dependency %r', dep_spec, exc_info=err)
                            continue
                        groups['dev'].add(normalize_packagename(req.name))

        lock_root = self.__get_lock_root(locker, root_name=None)
        if lock_root is not None:
            raw_lock = lock_root.package.get('dev-dependencies', {})
            if isinstance(raw_lock, dict):
                for group_raw, deps in raw_lock.items():
                    group = normalize_packagename(str(group_raw))
                    groups.setdefault(group, set())
                    for dep in deps or ():
                        if isinstance(dep, dict) and 'name' in dep:
                            groups[group].add(normalize_packagename(str(dep['name'])))

        # uv defaults to syncing the `dev` group; treat it as existing even if empty.
        groups.setdefault('dev', set())

        return {k: frozenset(v) for k, v in groups.items()}

    def __get_default_groups(self, pyproject: 'T_NameDict', available_groups: frozenset[str]) -> frozenset[str]:
        default_groups = frozenset({'dev', })  # uv default

        tool = pyproject.get('tool', {})
        if isinstance(tool, dict):
            tool_uv = tool.get('uv', {})
            if isinstance(tool_uv, dict) and 'default-groups' in tool_uv:
                raw = tool_uv.get('default-groups')
                if raw == 'all':
                    default_groups = available_groups
                elif isinstance(raw, list):
                    default_groups = frozenset(
                        normalize_packagename(str(g))
                        for g in raw
                        if g
                    )
                elif isinstance(raw, str) and raw:
                    default_groups = frozenset({normalize_packagename(raw), })

        unknown = default_groups - available_groups
        if unknown:
            self._logger.warning('skip unknown default groups: %s', ', '.join(sorted(unknown)))
            default_groups = default_groups - unknown

        return default_groups

    def __group_dependency_specs(self, pyproject: 'T_NameDict', group: str) -> tuple[str, ...]:
        group_n = normalize_packagename(group)
        specs: list[str] = []

        raw = pyproject.get('dependency-groups', {})
        if isinstance(raw, dict):
            for group_raw, dep_specs in raw.items():
                if normalize_packagename(str(group_raw)) != group_n:
                    continue
                specs.extend(str(d) for d in (dep_specs or ()) if d)

        # legacy field; included in the `dev` group
        if group_n == 'dev':
            tool = pyproject.get('tool', {})
            if isinstance(tool, dict):
                tool_uv = tool.get('uv', {})
                if isinstance(tool_uv, dict):
                    legacy_dev = tool_uv.get('dev-dependencies', ())
                    if isinstance(legacy_dev, list):
                        specs.extend(str(d) for d in legacy_dev or () if d)

        return tuple(specs)

    def __group_dependencies(self, pyproject: 'T_NameDict', locker: 'T_NameDict', group: str) -> dict[str, set[str]]:
        """
        Best-effort group dependencies from `uv.lock`.

        Returns mapping of dependency-name to required extras.
        """
        del pyproject  # reserved for potential future use

        lock_root = self.__get_lock_root(locker, root_name=None)
        if lock_root is None:
            return {}
        raw = lock_root.package.get('dev-dependencies', {})
        if not isinstance(raw, dict):
            return {}
        group_n = normalize_packagename(group)

        deps: dict[str, set[str]] = {}
        for group_raw, group_deps in raw.items():
            if normalize_packagename(str(group_raw)) != group_n:
                continue
            for dep in group_deps or ():
                if not isinstance(dep, dict) or 'name' not in dep:
                    continue
                if not self.__is_marker_ok(dep.get('marker')):
                    continue
                dep_name = normalize_packagename(str(dep['name']))
                dep_extras_raw = dep.get('extra', dep.get('extras'))
                if isinstance(dep_extras_raw, list):
                    deps.setdefault(dep_name, set()).update(
                        normalize_packagename(str(e)) for e in dep_extras_raw if e
                    )
                else:
                    deps.setdefault(dep_name, set())
        return deps

    def __optional_dependencies_from_lock(self, lock_root_package: 'T_NameDict') -> dict[str, set[str]]:
        optional_deps: dict[str, set[str]] = {}
        raw = lock_root_package.get('optional-dependencies', {})
        if not isinstance(raw, dict):
            return optional_deps
        for extra_raw, deps in raw.items():
            extra = normalize_packagename(str(extra_raw))
            optional_deps.setdefault(extra, set())
            for dep in deps or ():
                if not isinstance(dep, dict) or 'name' not in dep:
                    continue
                if not self.__is_marker_ok(dep.get('marker'), extra=extra):
                    continue
                optional_deps.setdefault(extra, set()).add(normalize_packagename(str(dep['name'])))
        return optional_deps

    @dataclass(frozen=True)
    class _LockRoot:
        package: 'T_NameDict'
        dependencies: frozenset[str]

    def __get_lock_root(self, locker: 'T_NameDict', *, root_name: Optional[str]) -> Optional['_LockRoot']:
        """
        Best-effort lookup of the "root" package entry in `uv.lock`.

        Currently, uv includes the project as a local package, e.g. `source = { virtual = "." }` or
        `source = { editable = "." }`.
        """
        packages = locker.get('package', ())
        if not isinstance(packages, list):
            return None
        root_name_n = normalize_packagename(root_name) if root_name else None

        def is_project_source(pkg: 'T_NameDict') -> bool:
            source = pkg.get('source', {})
            if not isinstance(source, dict):
                return False
            for k in ('virtual', 'editable', 'path', 'directory'):
                if k in source and str(source.get(k)) in {'.', './'}:
                    return True
            return False

        candidate = None
        for pkg in packages:
            if not isinstance(pkg, dict):
                continue
            if root_name_n is not None and normalize_packagename(str(pkg.get('name', ''))) != root_name_n:
                continue
            if is_project_source(pkg):
                candidate = pkg
                break
            if candidate is None:
                candidate = pkg
        if candidate is None:
            return None

        deps = frozenset(
            normalize_packagename(str(d['name']))
            for d in candidate.get('dependencies', ())
            if isinstance(d, dict) and 'name' in d and self.__is_marker_ok(d.get('marker'))
        )
        return self._LockRoot(candidate, deps)

    def _make_bom(self, root_c: Component, locker: 'T_NameDict',
                  seed_deps: tuple[frozenset[str], dict[str, frozenset[str]]],
                  use_extras: frozenset[str]) -> 'Bom':
        bom = make_bom()
        bom.metadata.component = root_c
        self._logger.debug('root-component: %r', root_c)

        if use_extras:
            root_c.properties.update(
                Property(
                    name=PropertyName.PythonPackageExtra.value,
                    value=extra
                ) for extra in use_extras
            )

        lock_data: dict[str, list[_LockEntry]] = {}
        for entry in self._parse_lock(locker):
            _ld = lock_data.setdefault(entry.name, [])
            _ldl = len(_ld)
            if _ldl > 0 and entry.component.bom_ref.value:
                entry.component.bom_ref.value += f'#{_ldl}'
            _ld.append(entry)

        root_name_n = normalize_packagename(root_c.name)
        seed_names, required_extras = seed_deps
        for dep_name, extras in required_extras.items():
            for lock_entry in lock_data.get(dep_name, ()):
                lock_entry.component.properties.update(
                    Property(
                        name=PropertyName.PythonPackageExtra.value,
                        value=extra
                    ) for extra in extras
                )

        included = self.__collect_lock_entries(lock_data, seed_names, root_name_n)

        root_dep = Dependency(root_c.bom_ref)
        bom.dependencies.add(root_dep)

        def deps_for_name(dep_name_n: str) -> Iterable[_LockEntry]:
            if dep_name_n == root_name_n:
                return ()
            return lock_data.get(dep_name_n, ())

        for dep_name_n in sorted(seed_names):
            entries = deps_for_name(dep_name_n)
            if not entries:
                self._logger.warning('skip unlocked dependency: %s', dep_name_n)
                continue
            for entry in entries:
                root_dep.dependencies.add(Dependency(entry.component.bom_ref))

        deps_by_ref: dict[str, Dependency] = {root_c.bom_ref.value: root_dep}

        for entry in included:
            if entry.name == root_name_n:
                continue
            if not entry.added2bom:
                entry.added2bom = True
                self._logger.info('add component for package %r', entry.component.name)
                self._logger.debug('add component: %r', entry.component)
                bom.components.add(entry.component)
            dep = deps_by_ref.get(entry.component.bom_ref.value)
            if dep is None:
                dep = deps_by_ref[entry.component.bom_ref.value] = Dependency(entry.component.bom_ref)
                bom.dependencies.add(dep)

        for entry in included:
            if entry.name == root_name_n:
                continue
            dep = deps_by_ref.get(entry.component.bom_ref.value)
            if dep is None:
                continue
            for dep_name_n in sorted(entry.dependencies):
                if dep_name_n == root_name_n:
                    dep.dependencies.add(Dependency(root_c.bom_ref))
                    continue
                dep_entries = lock_data.get(dep_name_n)
                if dep_entries is None:
                    self._logger.warning('skip unlocked component: %s', dep_name_n)
                    continue
                for dep_entry in dep_entries:
                    dep.dependencies.add(Dependency(dep_entry.component.bom_ref))

        return bom

    def __collect_lock_entries(self, lock_data: dict[str, list[_LockEntry]],
                               seed_names: Iterable[str],
                               root_name: str) -> tuple[_LockEntry, ...]:
        included: dict[str, _LockEntry] = {}
        pending = list(sorted(seed_names))
        while pending:
            name = pending.pop()
            if name == root_name:
                continue
            entries = lock_data.get(name)
            if not entries:
                continue
            for entry in entries:
                ref = entry.component.bom_ref.value
                if ref in included:
                    continue
                included[ref] = entry
                pending.extend(sorted(entry.dependencies))
        return tuple(sorted(included.values(), key=lambda e: e.component.bom_ref.value))

    def _parse_lock(self, locker: 'T_NameDict') -> Generator[_LockEntry, None, None]:
        package: 'T_NameDict'
        for package in locker.get('package', []):
            res_markers = package.get('resolution-markers')
            if isinstance(res_markers, list) and len(res_markers) > 0:
                if self.__active_resolution_markers is not None:
                    if not any(str(m) in self.__active_resolution_markers for m in res_markers):
                        if not any(self.__is_marker_ok(m) for m in res_markers):
                            continue
                elif not any(self.__is_marker_ok(m) for m in res_markers):
                    continue
            yield _LockEntry(
                name=normalize_packagename(str(package['name'])),
                component=self.__make_component4lock(package),
                dependencies=frozenset(
                    normalize_packagename(str(d['name']))
                    for d in package.get('dependencies', ())
                    if isinstance(d, dict) and 'name' in d and self.__is_marker_ok(d.get('marker'))
                ),
                added2bom=False,
            )

    def __make_component4lock(self, package: 'T_NameDict') -> Component:
        source = package.get('source', {})
        is_local = isinstance(source, dict) and (
            'virtual' in source or 'editable' in source or 'path' in source or 'directory' in source
        )

        version = package.get('version')
        bom_ref = f'{package["name"]}@{version}' if version else str(package['name'])

        return Component(
            type=ComponentType.LIBRARY,
            bom_ref=bom_ref,
            name=package['name'],
            version=version,
            external_references=self.__extrefs4lock(package),
            purl=PackageURL(
                type=PurlTypePypi,
                name=package['name'],
                version=version,
                qualifiers=self.__purl_qualifiers4lock(package)
            ) if not is_local else None
        )

    def __purl_qualifiers4lock(self, package: 'T_NameDict') -> 'T_NameDict':
        qs: 'T_NameDict' = {}

        source = package.get('source', {})
        if not isinstance(source, dict):
            return qs

        if 'registry' in source:
            source_url = redact_auth_from_url(str(source.get('registry', '')).rstrip('/'))
            if source_url and '://pypi.org/' not in source_url:
                qs['repository_url'] = source_url
        elif 'url' in source:
            source_url = redact_auth_from_url(str(source.get('url', '')))
            if source_url and '://files.pythonhosted.org/' not in source_url:
                qs['download_url'] = source_url
        elif 'git' in source:
            # best-effort: uv lock format might evolve; keep this flexible.
            url = redact_auth_from_url(str(source.get('git', '')))
            rev = str(source.get('rev', source.get('reference', source.get('tag', ''))))
            qs['vcs_url'] = f'git+{url}@{rev}' if rev else f'git+{url}'

        return qs

    def __extrefs4lock(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        if isinstance(sdist := package.get('sdist'), dict) and 'url' in sdist:
            try:
                yield ExternalReference(
                    comment='sdist',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(redact_auth_from_url(str(sdist['url']))),
                    hashes=[HashType.from_composite_str(str(sdist['hash']))] if 'hash' in sdist else None
                )
            except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
                self._logger.debug('skipped sdist-extRef for: %r', package.get('name'), exc_info=error)
                del error

        wheels = package.get('wheels', ())
        if isinstance(wheels, list):
            for wheel in wheels:
                if not isinstance(wheel, dict) or 'url' not in wheel:
                    continue
                try:
                    yield ExternalReference(
                        comment='wheel',
                        type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(redact_auth_from_url(str(wheel['url']))),
                        hashes=[HashType.from_composite_str(str(wheel['hash']))] if 'hash' in wheel else None
                    )
                except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
                    self._logger.debug('skipped wheel-extRef for: %r', package.get('name'), exc_info=error)
                    del error
