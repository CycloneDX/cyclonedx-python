# This file is part of CycloneDX Python Lib
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
from dataclasses import dataclass
from itertools import chain
from os.path import join
from re import compile as re_compile
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable, List, Optional, Set, Tuple

from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
from cyclonedx.model.component import Component, ComponentScope
from packageurl import PackageURL

from . import BomBuilder, PropertyName
from .cli_common import add_argument_mc_type
from .utils.cdx import make_bom
from .utils.poetry import poetry2component
from .utils.secret import redact_auth_from_url
from .utils.toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import ComponentType

    NameDict = Dict[str, Any]


@dataclass
class _LockEntry:
    name: str
    component: 'Component'
    dependencies: Set[str]
    extra_deps: Dict[str, Set[str]]
    added2bom: bool
    added2bom_extras: Set[str]


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


class PoetryBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(description=dedent("""\
                           Build an SBOM from Poetry project.

                           The options and switches mimic the respective ones from Poetry CLI.
                           """),
                           **kwargs)
        # the options and switches SHALL mimic the ones from Poetry, which uses comma-separated lists and multi-use
        p.add_argument('--without',
                       metavar='<groups>',
                       help='The dependency groups to ignore (multiple values allowed)',
                       action='append',
                       dest='groups_without',
                       default=[])
        p.add_argument('--with',
                       metavar='<groups>',
                       help='The optional dependency groups to include (multiple values allowed)',
                       action='append',
                       dest='groups_with',
                       default=[])
        og = p.add_mutually_exclusive_group()
        og.add_argument('--only',
                        metavar='<groups>',
                        help='The only dependency groups to include (multiple values allowed)',
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
                        help='Extra sets of dependencies to include (multiple values allowed)',
                        action='append',
                        dest='extras',
                        default=[])
        eg.add_argument('--all-extras',
                        help='Include all extra dependencies (default: %(default)s)',
                        action='store_true',
                        dest='all_extras',
                        default=False)
        del eg
        add_argument_mc_type(p)
        p.add_argument('project_directory',
                       metavar='<project-directory>',
                       help='The project directory for Poetry (default: current working directory)',
                       nargs=OPTIONAL,
                       default='.')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **__: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 project_directory: str,
                 groups_without: List[str], groups_with: List[str], groups_only: List[str],
                 no_dev: bool,
                 extras: List[str], all_extras: bool,
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        pyproject_file = join(project_directory, 'pyproject.toml')
        lock_file = join(project_directory, 'poetry.lock')
        try:
            pyproject = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
        except OSError as err:
            raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
        try:
            lock = open(lock_file, 'rt', encoding='utf8', errors='replace')
        except OSError as err:
            pyproject.close()
            raise ValueError(f'Could not open lock file: {lock_file}') from err

        with pyproject, lock:
            project = toml_loads(pyproject.read())
            po_cfg = project['tool']['poetry']
            po_cfg.setdefault('group', {})
            po_cfg['group'].setdefault('main', {'dependencies': po_cfg.get('dependencies', {})})
            po_cfg['group'].setdefault('dev', {'dependencies': po_cfg.get('dev-dependencies', {})})
            po_cfg.setdefault('extras', {})

            # the group-args shall mimic the ones from poetry, which uses comma-separated lists and multi-use
            # values be like: ['foo', 'bar,bazz'] -> ['foo', 'bar', 'bazz']
            groups_only_s = set(filter(None, ','.join(groups_only).split(',')))
            groups_with_s = set(filter(None, ','.join(groups_with).split(',')))
            groups_without_s = set(filter(None, ','.join(groups_without).split(',')))
            del groups_only, groups_with, groups_without
            groups_not_found = set(
                (gn, srcn) for gns, srcn in [
                    (groups_only_s, 'only'),
                    (groups_with_s, 'with'),
                    (groups_without_s, 'without'),
                ] for gn in gns
                if gn not in po_cfg['group'].keys())
            if len(groups_not_found) > 0:
                groups_error = GroupsNotFoundError(f'{gn!r} (via {srcn})' for gn, srcn in groups_not_found)
                self._logger.error(groups_error)
                raise ValueError('some Poetry groups are unknown') from groups_error
            del groups_not_found

            extras_s = set(filter(None, ','.join(extras).split(',')))
            del extras
            extras_defined = set(po_cfg['extras'].keys())
            extras_not_found = extras_s - extras_defined
            if len(extras_not_found) > 0:
                extras_error = ExtrasNotFoundError(extras_not_found)
                self._logger.error(extras_error)
                raise ValueError('some package extras are unknown') from extras_error
            del extras_not_found

            # the group-args shall mimic the ones from Poetry.
            # Poetry handles this pseudo-exclusive-group of args programmatically
            if no_dev:
                groups = {'main', }
            elif len(groups_only_s) > 0:
                groups = groups_only_s
            else:
                # When used together, `--without` takes precedence over `--with`.
                # see https://python-poetry.org/docs/managing-dependencies/#installing-group-dependencies
                groups = set(
                    gn for gn, gc in po_cfg['group'].items()
                    # all non-optionals and the `with`-whitelisted optionals
                    if not gc.get('optional') or gn in groups_with_s
                ) - groups_without_s
            del groups_only_s, groups_with_s, groups_without_s

            return self._make_bom(
                project, toml_loads(lock.read()),
                groups,
                extras_defined if all_extras else extras_s,
                mc_type,
            )

    def _make_bom(self, project: 'NameDict', locker: 'NameDict',
                  use_groups: Set[str], use_extras: Set[str],
                  mc_type: 'ComponentType') -> 'Bom':
        self._logger.debug('use_groups: %r', use_groups)
        self._logger.debug('use_extras: %r', use_extras)

        bom = make_bom()

        po_cfg = project['tool']['poetry']

        bom.metadata.component = root_c = poetry2component(po_cfg, type=mc_type)
        root_c.bom_ref.value = root_c.name  # 'root-component'
        root_c.properties.update(Property(
            name=PropertyName.PackageExtra.value,
            value=extra
        ) for extra in use_extras)
        self._logger.debug('root-component: %r', root_c)

        lock_data: Dict[str, _LockEntry] = {le.name.lower(): le for le in self._parse_lock(locker)}

        lock_data[root_c.name] = _LockEntry(  # needed for circle dependencies
            name=root_c.name,
            component=root_c,
            dependencies=set(),
            extra_deps={},
            added2bom=True,
            added2bom_extras=use_extras
        )
        extra_deps = set(map(str.lower, chain.from_iterable(po_cfg['extras'][extra] for extra in use_extras)))

        _dep_pattern = re_compile(r'^(?P<name>[^\[]+)(?:\[(?P<extras>.*)\])?$')

        lock_version = self._get_lockfile_version(locker)
        should_tidy_lock_names = lock_version >= (2,)

        def _add_ld(name: str, extras: Set[str]) -> Optional['Component']:
            name = name.lower()
            if name == 'python':
                return None
            if should_tidy_lock_names:
                name = name.replace('.', '-')
            le = lock_data.get(name)
            if le is None:
                self._logger.warning('skip unlocked component: %s', name)
                return None
            _existed = le.added2bom
            if _existed:
                self._logger.debug('existing component: %r', le.component)
            else:
                self._logger.info('add component for package %r', name)
                self._logger.debug('add component: %r', le.component)
                le.added2bom = True
                bom.components.add(le.component)
            new_extras = extras - le.added2bom_extras
            self._logger.debug('new extras for %r: %r', le.component, new_extras)
            le.added2bom_extras.update(new_extras)
            le.component.properties.update(Property(
                name=PropertyName.PackageExtra.value,
                value=extra
            ) for extra in new_extras)
            depends_on: List[Optional['Component']] = []
            for dep in set(chain(
                () if _existed else le.dependencies,
                chain.from_iterable(le.extra_deps.get(extra, ()) for extra in new_extras)
            )):
                self._logger.debug('component %r depends on %r', le.component, dep)
                depm = _dep_pattern.match(dep)
                if depm is None:  # pragma: nocover
                    self._logger.warning('skipping malformed dependency: %r', dep)
                    continue
                depends_on.append(_add_ld(
                    depm.group('name'),
                    set(filter(None, map(str.strip, (depm.group('extras') or '').split(','))))
                ))
            bom.register_dependency(le.component, filter(None, depends_on))
            return le.component

        depends_on: List[Optional['Component']] = []
        for group_name in use_groups:
            self._logger.debug('processing group %r ...', group_name)
            for dep_name, dep_spec in po_cfg['group'][group_name].get('dependencies', {}).items():
                dep_name = dep_name.lower()
                if should_tidy_lock_names:
                    dep_name = dep_name.replace('.', '-')
                self._logger.debug('root-component depends on %s', dep_name)
                if dep_name == 'python':
                    continue
                if dep_name not in lock_data:
                    self._logger.warning('skip unlocked dependency: %s', dep_name)
                    continue
                lock_data[dep_name].component.properties.add(Property(
                    name=PropertyName.PoetryGroup.value,
                    value=group_name
                ))
                dep_spec = dep_spec if isinstance(dep_spec, dict) else {'version': dep_spec}
                if dep_spec.get('optional', False) and dep_name not in extra_deps:
                    self._logger.debug('skip optional dependency: %s', dep_name)
                    continue
                depends_on.append(_add_ld(dep_name, set(dep_spec.get('extras', ()))))
        bom.register_dependency(root_c, filter(None, depends_on))

        return bom

    @staticmethod
    def _get_lockfile_version(locker: 'NameDict') -> Tuple[int, ...]:
        return tuple(int(v) for v in locker['metadata'].get('lock-version', '1.0').split('.'))

    def _parse_lock(self, locker: 'NameDict') -> Generator[_LockEntry, None, None]:
        locker.setdefault('metavar', {})
        locker.setdefault('package', [])

        lock_version = self._get_lockfile_version(locker)
        self._logger.debug('lock_version: %r', lock_version)

        metavar_files = locker['metadata'].get('files', {}) if lock_version < (2,) else {}

        package: 'NameDict'
        for package in locker['package']:
            package.setdefault('files', metavar_files.get(package['name'], []))
            package.setdefault('source', {})
            yield _LockEntry(
                name=package['name'],
                component=self.__make_component4lock(package),
                dependencies=set(dn for dn, ds in package.get('dependencies', {}).items()
                                 if not isinstance(ds, dict) or not ds.get('optional', False)),
                extra_deps={en: set(di.split(' ')[0] for di in ds) for en, ds in package.get('extras', {}).items()},
                added2bom=False,
                added2bom_extras=set()
            )

    __PACKAGE_SRC_VCS = ['git']  # not supported yet: hg, svn
    __PACKAGE_SRC_LOCAL = ['file', 'directory']

    def __make_component4lock(self, package: 'NameDict') -> 'Component':
        source = package['source']
        is_vcs = source.get('type') in self.__PACKAGE_SRC_VCS
        is_local = source.get('type') in self.__PACKAGE_SRC_LOCAL

        return Component(
            bom_ref=f'{package["name"]}@{package["version"]}',
            name=package['name'],
            version=package.get('version'),
            description=package.get('description'),
            scope=ComponentScope.OPTIONAL if package.get('optional') else None,
            external_references=self.__extrefs4lock(package),
            properties=filter(lambda p: p and p.value, [  # type: ignore[arg-type]
                Property(  # for backwards compatibility: category -> group
                    name=PropertyName.PoetryGroup.value,
                    value=package['category']
                ) if 'category' in package else None,
                Property(
                    name=PropertyName.PoetryPackageSourceReference.value,
                    value=source['reference']
                ) if is_vcs and 'reference' in source else None,
                Property(
                    name=PropertyName.PoetryPackageSourceResolvedReference.value,
                    value=source['resolved_reference']
                ) if is_vcs and 'resolved_reference' in source else None,
            ]),
            purl=PackageURL(type='pypi',
                            name=package['name'],
                            version=package['version'],
                            qualifiers=self.__purl_qualifiers4lock(package)
                            ) if not is_local else None
        )

    def __purl_qualifiers4lock(self, package: 'NameDict') -> 'NameDict':
        # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
        qs = {}

        source = package['source']
        source_type = package['source'].get('type')

        if source_type in self.__PACKAGE_SRC_VCS:
            # see section 3.7.4 in https://github.com/spdx/spdx-spec/blob/cfa1b9d08903/chapters/3-package-information.md
            # > For version-controlled files, the VCS location syntax is similar to a URL and has the:
            # > `<vcs_tool>+<transport>://<host_name>[/<path_to_repository>][@<revision_tag_or_branch>][#<sub_path>]`
            qs['vcs_url'] = f'{source["type"]}+{redact_auth_from_url(source["url"])}@' + \
                source.get('resolved_reference', source.get('reference', ''))
        elif source_type == 'url':
            if '://files.pythonhosted.org/' not in source['url']:
                # skip PURL bloat, do not add implicit information
                qs['download_url'] = redact_auth_from_url(source['url'])
        elif source_type == 'legacy':
            source_url = package['source'].get('url', 'https://pypi.org/simple')
            if '://pypi.org/' not in source_url:
                # skip PURL bloat, do not add implicit information
                qs['repository_url'] = redact_auth_from_url(source_url)

        return qs

    def __extrefs4lock(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        source_type = package['source'].get('type', 'legacy')
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

    def __extrefs4lock_legacy(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        source_url = redact_auth_from_url(package['source'].get('url', 'https://pypi.org/simple'))
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

    def __extrefs4lock_url(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from url',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url'])),
                hashes=[HashType.from_composite_str(package['files'][0]['hash'])] if len(package['files']) else None
            )
        except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_file(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from file',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url'])),
                hashes=[HashType.from_composite_str(package['files'][0]['hash'])] if len(package['files']) else None
            )
        except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_directory(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        try:
            yield ExternalReference(
                comment='from directory',
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(redact_auth_from_url(package['source']['url']))
                # no hash for a source-directory
            )
        except InvalidUriException as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', package['name'], exc_info=error)

    def __extrefs4lock_vcs(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
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
