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
from itertools import chain
from os.path import join
from re import compile as re_compile
from textwrap import dedent
from typing import TYPE_CHECKING, Any

from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
from cyclonedx.model.component import Component, ComponentScope
from cyclonedx.model.dependency import Dependency
from packageurl import PackageURL

from . import BomBuilder, PropertyName, PurlTypePypi
from .cli_common import add_argument_mc_type
from .utils.cdx import make_bom
from .utils.packaging import normalize_packagename
from .utils.poetry import poetry2component
from .utils.secret import redact_auth_from_url
from .utils.toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import ComponentType

    T_NameDict = dict[str, Any]
    T_LockData = dict[str, list['_LockEntry']]


@dataclass
class _LockEntry:
    name: str
    component: Component
    dependencies: dict[str, 'T_NameDict']  # keys MUST go through `normalize_packagename()`
    extras: dict[str, list[str]]  # keys MUST go through `normalize_packagename()`
    added2bom: bool


class GroupsNotFoundError(ValueError):
    def __init__(self, groups: Iterable[str]) -> None:
        self.__groups = frozenset(groups)

    def __str__(self) -> str:
        return 'Group(s) not found: ' + ', '.join(sorted(self.__groups))


class ExtrasNotFoundError(ValueError):
    def __init__(self, extras: Iterable[str]) -> None:
        self.__extras = frozenset(extras)

    def __str__(self) -> str:
        return f'Extra(s) [{",".join(sorted(self.__extras))}] not specified.'


@dataclass(frozen=True)
class _PoetryPackageRequirement:
    name: str
    extras: set[str]

    # the pattern is good enough for the job
    __lock_pattern = re_compile(r'^([a-zA-Z0-9._-]+)(?:\[(.+?)\])?')

    @classmethod
    def from_poetry_lock(cls: type['_PoetryPackageRequirement'], r: str) -> '_PoetryPackageRequirement':
        matches = cls.__lock_pattern.match(r)
        if matches is None:
            raise ValueError(f'cannot parse: {r}')
        # ! no normalization is done here - this is just a data structure, nothing more
        return cls(
            matches[1],
            set(matches[2].split(',') if matches[2] else ())
        )


class PoetryBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(
            description=dedent("""\
                Build an SBOM from Poetry project.

                The options and switches mimic the respective ones from Poetry CLI.
                """),
            **kwargs)
        # the options and switches SHALL mimic the ones from Poetry, which uses comma-separated lists and multi-use
        p.add_argument('--without',
                       metavar='<groups>',
                       help='The dependency groups to ignore'
                            ' (multiple values allowed)',
                       action='append',
                       dest='groups_without',
                       default=[])
        p.add_argument('--with',
                       metavar='<groups>',
                       help='The optional dependency groups to include'
                            ' (multiple values allowed)',
                       action='append',
                       dest='groups_with',
                       default=[])
        og = p.add_mutually_exclusive_group()
        og.add_argument('--only',
                        metavar='<groups>',
                        help='The only dependency groups to include'
                             ' (multiple values allowed)',
                        action='append',
                        dest='groups_only',
                        default=[])
        og.add_argument('--no-dev',
                        help='Alias for: --only main',
                        dest='no_dev',
                        action='store_true')
        del og
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
                       help='The project directory for Poetry'
                            ' (default: current working directory)',
                       nargs=OPTIONAL,
                       default='.')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **__: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 project_directory: str,
                 groups_without: list[str], groups_with: list[str], groups_only: list[str],
                 no_dev: bool,
                 extras: list[str], all_extras: bool,
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        pyproject_file = join(project_directory, 'pyproject.toml')
        lock_file = join(project_directory, 'poetry.lock')
        try:
            pyproject = open(pyproject_file, encoding='utf8', errors='replace')
        except OSError as err:
            raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
        try:
            lock = open(lock_file, encoding='utf8', errors='replace')
        except OSError as err:
            pyproject.close()
            raise ValueError(f'Could not open lock file: {lock_file}') from err

        with pyproject, lock:
            project = toml_loads(pyproject.read())
            po_cfg = project['tool']['poetry']
            po_cfg_group = po_cfg.setdefault('group', {})
            po_cfg_group.setdefault('main', {'dependencies': po_cfg.get('dependencies', {})})
            po_cfg_group.setdefault('dev', {'dependencies': po_cfg.get('dev-dependencies', {})})
            po_cfg_extras = po_cfg['extras'] = {
                normalize_packagename(en): es
                for en, es in po_cfg.get('extras', {}).items()
            }

            # the group-args shall mimic the ones from poetry, which uses comma-separated lists and multi-use
            # values be like: ['foo', 'bar,bazz'] -> ['foo', 'bar', 'bazz']
            groups_only_s = frozenset(filter(None, ','.join(groups_only).split(',')))
            groups_with_s = frozenset(filter(None, ','.join(groups_with).split(',')))
            groups_without_s = frozenset(filter(None, ','.join(groups_without).split(',')))
            del groups_only, groups_with, groups_without
            groups_not_found = frozenset(
                (gn, srcn) for gns, srcn in [
                    (groups_only_s, 'only'),
                    (groups_with_s, 'with'),
                    (groups_without_s, 'without'),
                ] for gn in gns
                if gn not in po_cfg_group)
            if len(groups_not_found) > 0:
                groups_error = GroupsNotFoundError(f'{gn!r} (via {srcn})' for gn, srcn in groups_not_found)
                self._logger.error(groups_error)
                raise ValueError('some Poetry groups are unknown') from groups_error
            del groups_not_found

            if all_extras:
                extras_s = frozenset(po_cfg_extras)
            else:
                extras_s = frozenset(map(normalize_packagename,
                                         # values be like: ['foo', 'bar,bazz'] -> ['foo', 'bar', 'bazz']
                                         filter(None, ','.join(extras).split(','))))
                extras_not_found = extras_s - po_cfg_extras.keys()
                if len(extras_not_found) > 0:
                    extras_error = ExtrasNotFoundError(extras_not_found)
                    self._logger.error(extras_error)
                    raise ValueError('some package extras are unknown') from extras_error
                del extras_not_found
            del extras

            # the group-args shall mimic the ones from Poetry.
            # Poetry handles this pseudo-exclusive-group of args programmatically
            if no_dev:
                groups = frozenset({'main', })
            elif len(groups_only_s) > 0:
                groups = groups_only_s
            else:
                # When used together, `--without` takes precedence over `--with`.
                # see https://python-poetry.org/docs/managing-dependencies/#installing-group-dependencies
                groups = frozenset(
                    gn for gn, gc in po_cfg['group'].items()
                    # all non-optionals and the `with`-whitelisted optionals
                    if not gc.get('optional') or gn in groups_with_s
                ) - groups_without_s
            del groups_only_s, groups_with_s, groups_without_s

            return self._make_bom(
                project, toml_loads(lock.read()),
                groups,
                extras_s,
                mc_type,
            )

    def _make_bom(self, project: 'T_NameDict', locker: 'T_NameDict',
                  use_groups: frozenset[str], use_extras: frozenset[str],
                  mc_type: 'ComponentType') -> 'Bom':
        self._logger.debug('use_groups: %r', use_groups)
        self._logger.debug('use_extras: %r', use_extras)

        bom = make_bom()

        po_cfg = project['tool']['poetry']

        bom.metadata.component = root_c = poetry2component(po_cfg, ctype=mc_type)
        root_c.bom_ref.value = root_c.name
        root_c.properties.update(
            Property(
                name=PropertyName.PythonPackageExtra.value,
                value=extra
            ) for extra in use_extras
        )
        self._logger.debug('root-component: %r', root_c)
        root_d = Dependency(root_c.bom_ref)
        bom.dependencies.add(root_d)

        lock_data: 'T_LockData' = {}
        for lock_entry in self._parse_lock(locker):
            _ld = lock_data.setdefault(lock_entry.name, [])
            _ldl = len(_ld)
            if _ldl > 0 and lock_entry.component.bom_ref.value:
                # Best-effort for reproducibility: enumerate the potential duplicates.
                # To prevent auto-assigning names for duplicates when rendering the CycloneDX document.
                lock_entry.component.bom_ref.value += f'#{_ldl}'
            _ld.append(lock_entry)

        root_c_nname = normalize_packagename(root_c.name)
        lock_data[root_c_nname] = [_LockEntry(  # needed for circle dependencies
            name=root_c_nname,
            component=root_c,
            dependencies={},
            extras={},  # TODO - skipped unless a real-world case comes up
            added2bom=True,
        )]
        del root_c_nname

        use_extras_dep_names = frozenset(map(normalize_packagename,
                                             chain.from_iterable(po_cfg['extras'][e] for e in use_extras)))
        for group_name in use_groups:
            for dep_name, dep_specs in po_cfg['group'][group_name].get('dependencies', {}).items():
                dep_name = normalize_packagename(dep_name)
                if not isinstance(dep_specs, list):
                    if isinstance(dep_specs, dict):
                        dep_specs = [dep_specs]
                    else:
                        dep_specs = [{'version': dep_specs}]
                self._logger.debug('root-component depends on %s', dep_name)
                if dep_name == 'python':
                    continue  # skip python constraint
                lock_entries = lock_data.get(dep_name)
                if lock_entries is None:
                    self._logger.warning('skip unlocked dependency: %s', dep_name)
                    continue
                if all(ds.get('optional') for ds in dep_specs) and dep_name not in use_extras_dep_names:
                    self._logger.debug('skip optional unused dependency: %s', dep_name)
                    continue
                for lock_entry in lock_entries:
                    lock_entry.component.properties.add(Property(
                        name=PropertyName.PoetryGroup.value,
                        value=group_name
                    ))
                    root_d.dependencies.add(Dependency(lock_entry.component.bom_ref))
                    self.__add_dep(
                        bom, lock_entry,
                        chain.from_iterable(ds.get('extras', ()) for ds in dep_specs),
                        lock_data)

        return bom

    def __add_dep(self, bom: 'Bom', lock_entry: _LockEntry, use_extras: Iterable[str], lock_data: 'T_LockData') -> None:
        if lock_entry.added2bom:
            self._logger.debug('existing component: %r', lock_entry.component)
            lock_entry_dep = None
        else:
            lock_entry.added2bom = True
            self._logger.info('add component for package %r', lock_entry.name)
            self._logger.debug('add component: %r', lock_entry.component)
            bom.components.add(lock_entry.component)
            lock_entry_dep = Dependency(lock_entry.component.bom_ref)
            bom.dependencies.add(lock_entry_dep)
            for dep_name, dep_spec in lock_entry.dependencies.items():
                # Actually, a best-path should be calculated here, like it is done by Poetry itself...
                # This would require heavy computation and might cause false-negatives or insufficient picks.
                # Instead, we pick all dependencies, just to be on the safe side.
                dep_lock_entries = lock_data.get(dep_name)
                if dep_lock_entries is None:
                    self._logger.warning('skip unlocked component: %s', dep_name)
                    continue
                if dep_spec.get('optional'):
                    # optionals are not installed, per default. they may be added via `use_extras` later.
                    continue
                for dep_lock_entry in dep_lock_entries:
                    lock_entry_dep.dependencies.add(Dependency(dep_lock_entry.component.bom_ref))
                    self.__add_dep(bom, dep_lock_entry, dep_spec.get('extras', ()), lock_data)
        if use_extras:
            use_extras = frozenset(map(normalize_packagename, use_extras))
            lock_entry.component.properties.update(
                Property(
                    name=PropertyName.PythonPackageExtra.value,
                    value=extra
                ) for extra in use_extras
            )
            lock_entry_dep = lock_entry_dep \
                or next(filter(lambda d: d.ref is lock_entry.component.bom_ref, bom.dependencies))
            for req in map(
                _PoetryPackageRequirement.from_poetry_lock,
                chain.from_iterable(es for en, es in lock_entry.extras.items() if en in use_extras)
            ):
                dep_name = normalize_packagename(req.name)
                dep_lock_entries = lock_data.get(dep_name)
                if dep_lock_entries is None:
                    self._logger.warning('skip unlocked component: %s', dep_name)
                    continue
                for dep_lock_entry in dep_lock_entries:
                    lock_entry_dep.dependencies.add(Dependency(dep_lock_entry.component.bom_ref))
                    self.__add_dep(bom, dep_lock_entry, req.extras, lock_data)

    @staticmethod
    def _get_lockfile_version(locker: 'T_NameDict') -> tuple[int, ...]:
        return tuple(map(int, locker['metadata'].get('lock-version', '1.0').split('.')))

    def _parse_lock(self, locker: 'T_NameDict') -> Generator[_LockEntry, None, None]:
        lock_version = self._get_lockfile_version(locker)
        self._logger.debug('lock_version: %r', lock_version)
        metavar_files = locker.get('metadata', {}).get('files', {}) if lock_version < (2,) else {}
        package: 'T_NameDict'
        for package in locker.get('package', []):
            package.setdefault('files', metavar_files.get(package['name'], []))
            yield _LockEntry(
                name=normalize_packagename(package['name']),
                component=self.__make_component4lock(package),
                dependencies={
                    normalize_packagename(dn): ds if isinstance(ds, dict) else {'version': ds}
                    for dn, ds in package.get('dependencies', {}).items()
                },
                extras={
                    normalize_packagename(en): es
                    for en, es in package.get('extras', {}).items()
                },
                added2bom=False,
            )

    __PACKAGE_SRC_VCS = ['git']  # not supported yet: hg, svn
    __PACKAGE_SRC_LOCAL = ['file', 'directory']

    def __make_component4lock(self, package: 'T_NameDict') -> 'Component':
        source = package.get('source', {})
        is_vcs = source.get('type') in self.__PACKAGE_SRC_VCS
        is_local = source.get('type') in self.__PACKAGE_SRC_LOCAL

        return Component(
            bom_ref=f'{package["name"]}@{package["version"]}',
            name=package['name'],
            version=package.get('version'),
            description=package.get('description'),
            scope=ComponentScope.OPTIONAL if package.get('optional') else None,
            external_references=self.__extrefs4lock(package),
            properties=filter(lambda p: p and p.value, (  # type: ignore[arg-type]
                Property(
                    name=PropertyName.PythonPackageSourceVcsRequestedRevision.value,
                    value=source['reference']
                ) if is_vcs and 'reference' in source else None,
                Property(
                    name=PropertyName.PythonPackageSourceVcsCommitId.value,
                    value=source['resolved_reference']
                ) if is_vcs and 'resolved_reference' in source else None,
                Property(  # for backwards compatibility: category -> group
                    name=PropertyName.PoetryGroup.value,
                    value=package['category']
                ) if 'category' in package else None,
            )),
            purl=PackageURL(
                type=PurlTypePypi,
                name=package['name'],
                version=package['version'],
                qualifiers=self.__purl_qualifiers4lock(package)
            ) if not is_local else None
        )

    def __purl_qualifiers4lock(self, package: 'T_NameDict') -> 'T_NameDict':
        # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
        qs = {}

        source = package.get('source', {})
        source_type = source.get('type')

        if source_type in self.__PACKAGE_SRC_VCS:
            # see section 3.7.4 in https://github.com/spdx/spdx-spec/blob/cfa1b9d08903/chapters/3-package-information.md
            # > For version-controlled files, the VCS location syntax is similar to a URL and has the:
            # > `<vcs_tool>+<transport>://<host_name>[/<path_to_repository>][@<revision_tag_or_branch>][#<sub_path>]`
            qs['vcs_url'] = f'{source_type}+{redact_auth_from_url(source["url"])}@' + \
                source.get('resolved_reference', source.get('reference', ''))
        elif source_type == 'url':
            if '://files.pythonhosted.org/' not in source['url']:
                # skip PURL bloat, do not add implicit information
                qs['download_url'] = redact_auth_from_url(source['url'])
        elif source_type == 'legacy':
            source_url = source.get('url', 'https://pypi.org/simple')
            if '://pypi.org/' not in source_url:
                # skip PURL bloat, do not add implicit information
                qs['repository_url'] = redact_auth_from_url(source_url)

        return qs

    def __extrefs4lock(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        source_type = package.get('source', {}).get('type', 'legacy')
        if 'legacy' == source_type:
            yield from self.__extrefs4lock_legacy(package)
        elif 'url' == source_type:
            yield from self.__extrefs4lock_url(package)
        elif 'file' == source_type:
            yield from self.__extrefs4lock_file(package)
        elif 'directory' == source_type:
            yield from self.__extrefs4lock_directory(package)
        elif source_type in self.__PACKAGE_SRC_VCS:
            yield from self.__extrefs4lock_vcs(package)

    def __extrefs4lock_legacy(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        source_url = redact_auth_from_url(package.get('source', {}).get('url', 'https://pypi.org/simple'))
        for file in package['files']:
            try:
                yield ExternalReference(
                    comment='from legacy-api',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(f'{source_url}/{package["name"]}/#{file["file"]}'),
                    hashes=[HashType.from_composite_str(file['hash'])]
                )
            except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
                self._logger.debug('skipped dist-extRef for: %r | %r', package['name'], file, exc_info=error)
                del error

    def __extrefs4lock_url(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from url',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url'])),
                hashes=[HashType.from_composite_str(package['files'][0]['hash'])] if len(package['files']) else None
            )
        except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_file(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from file',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url'])),
                hashes=[HashType.from_composite_str(package['files'][0]['hash'])] if len(package['files']) else None
            )
        except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_directory(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from directory',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url']))
                # no hash for a source-directory
            )
        except InvalidUriException as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_vcs(self, package: 'T_NameDict') -> Generator['ExternalReference', None, None]:
        source = package['source']
        vcs_ref = source.get('resolved_reference', source.get('reference', ''))
        try:
            yield ExternalReference(
                comment='from VCS',
                type=ExternalReferenceType.VCS,
                url=XsUri(f'{source["type"]}+{redact_auth_from_url(source["url"])}#{vcs_ref}')
                # no hashes, has source.resolved_reference instead, which is a property
            )
        except InvalidUriException as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)
