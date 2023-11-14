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


from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable, List, Optional, Set

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model import ExternalReference, HashType
    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component, ComponentType

    NameDict = Dict[str, Any]


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


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
        from argparse import OPTIONAL, ArgumentParser
        from textwrap import dedent

        from cyclonedx.model.component import ComponentType

        from .utils.args import argparse_type4enum

        p = ArgumentParser(description=dedent('''\
                           Build an SBOM from Poetry project.

                           The options mimic the respective ones from Poetry.
                           '''),
                           **kwargs)
        # the args shall mimic the ones from Poetry, which uses comma-separated lists and multi-use
        p.add_argument('--without',
                       metavar='GROUPS',
                       help='The dependency groups to ignore (multiple values allowed)',
                       action='append',
                       dest='groups_without',
                       default=[])
        p.add_argument('--with',
                       metavar='GROUPS',
                       help='The optional dependency groups to include (multiple values allowed)',
                       action='append',
                       dest='groups_with',
                       default=[])
        p.add_argument('--only',
                       metavar='GROUPS',
                       help='The only dependency groups to include (multiple values allowed)',
                       action='append',
                       dest='groups_only',
                       default=[])
        p.add_argument('--no-dev',
                       help='Explicitly force: --only main',
                       dest='no_dev',
                       action='store_true')
        eg = p.add_mutually_exclusive_group()
        eg.add_argument('-E', '--extras',
                        metavar='EXTRAS',
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
        p.add_argument('project_directory',
                       metavar='project-directory',
                       help='The project directory for Poetry (default: current working directory)',
                       nargs=OPTIONAL,
                       default='.')
        _mc_types = [ComponentType.APPLICATION,
                     ComponentType.FIRMWARE,
                     ComponentType.LIBRARY]
        p.add_argument('--mc-type',
                       metavar='TYPE',
                       help='Type of the main component'
                            f' {{choice: {", ".join(t.value for t in _mc_types)}}}'
                            ' (default: %(default)s)',
                       dest='mc_type',
                       choices=_mc_types,
                       type=argparse_type4enum(ComponentType),
                       default=ComponentType.APPLICATION.value)
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 project_directory: str,
                 groups_without: List[str], groups_with: List[str], groups_only: List[str],
                 no_dev: bool,
                 extras: List[str], all_extras: bool,
                 mc_type: 'ComponentType',
                 **kwargs: Any) -> 'Bom':
        from os.path import join

        from .utils.toml import toml_loads

        pyproject_file = join(project_directory, 'pyproject.toml')
        lock_file = join(project_directory, 'poetry.lock')
        try:
            pyproject = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
        except OSError as err:
            raise ValueError(f"can't open {pyproject_file!r}: {err}")
        try:
            lock = open(lock_file, 'rt', encoding='utf8', errors='replace')
        except OSError as err:
            pyproject.close()
            raise ValueError(f"can't open {lock_file!r}: {err}")

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
            self._logger.debug('groups_not_found: %r', groups_not_found)
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
        from itertools import chain
        from re import compile as re_compile

        from cyclonedx.model import Property

        from . import PropertyName
        from .utils.bom import make_bom

        self._logger.debug('use_groups: %r', use_groups)
        self._logger.debug('use_extras: %r', use_extras)

        bom = make_bom()

        po_cfg = project['tool']['poetry']

        bom.metadata.component = root_c = self.__component4poetryproj(po_cfg, mc_type)
        root_c.properties.update(Property(
            name=PropertyName.PackageExtra.value,
            value=extra
        ) for extra in use_extras)
        self._logger.debug('root-component: %r', root_c)

        lock_data: Dict[str, _LockEntry] = {le.name: le for le in self._parse_lock(locker)}

        lock_data[root_c.name] = _LockEntry(  # needed for circle dependencies
            name=root_c.name,
            component=root_c,
            dependencies=set(),
            extra_deps=dict(),
            added2bom=True,
            added2bom_extras=use_extras
        )
        extra_deps = set(chain.from_iterable(po_cfg['extras'][extra] for extra in use_extras))

        _dep_pattern = re_compile(r'^(?P<name>[^\[]+)(?:\[(?P<extras>.*)\])?$')

        def _add_ld(name: str, extras: Set[str]) -> Optional['Component']:
            if name == 'python':
                return None
            le = lock_data.get(name)
            if le is None:
                self._logger.warning('skip unlocked component: %s', name)
                return None
            _existed = le.added2bom
            if _existed:
                self._logger.debug('existing component: %r', le.component)
            else:
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
            depends_on = []
            for dep in set(chain(
                [] if _existed else le.dependencies,
                chain.from_iterable(le.extra_deps.get(extra, []) for extra in new_extras)
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

        depends_on = []
        for group_name in use_groups:
            self._logger.debug('processing group %r ...', group_name)
            for dep_name, dep_spec in po_cfg['group'][group_name].get('dependencies', {}).items():
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
                depends_on.append(_add_ld(dep_name, set(dep_spec.get('extras', []))))
        bom.register_dependency(root_c, filter(None, depends_on))

        return bom

    def __component4poetryproj(self, po_cfg: 'NameDict', c_type: 'ComponentType') -> 'Component':
        from cyclonedx.exception.model import InvalidUriException
        from cyclonedx.factory.license import LicenseFactory
        from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri
        from cyclonedx.model.component import Component

        # see spec: https://python-poetry.org/docs/pyproject/
        comp = Component(
            bom_ref=str(po_cfg.get('name', 'root-component')),
            type=c_type,
            name=str(po_cfg.get('name', 'unnamed')),
            version=str(po_cfg.get('version', '')) or None,
            description=str(po_cfg.get('description', '')) or None,
            licenses=[LicenseFactory().make_from_string(po_cfg['license'])] if 'license' in po_cfg else None,
            author=' | '.join(po_cfg['authors']) if 'authors' in po_cfg else None,
        )
        for ers, ert in [
            ('homepage', ExternalReferenceType.WEBSITE),
            ('repository', ExternalReferenceType.VCS),
            ('documentation', ExternalReferenceType.DOCUMENTATION),
        ]:
            try:
                ExternalReference(type=ert, url=XsUri(str(po_cfg[ers])))
            except (KeyError, InvalidUriException):
                pass
        known_ulr_names = {
            'bug tracker': ExternalReferenceType.ISSUE_TRACKER,
            'issue tracker': ExternalReferenceType.ISSUE_TRACKER,
        }
        for un, ul in po_cfg.get('urls', {}).items():
            try:
                ExternalReference(type=known_ulr_names.get(un.lower(), ExternalReferenceType.OTHER),
                                  url=XsUri(str(ul)), comment=un)
            except InvalidUriException:
                pass
        return comp

    def _parse_lock(self, locker: 'NameDict') -> Generator[_LockEntry, None, None]:
        locker.setdefault('metavar', {})
        locker.setdefault('package', [])

        lock_version = tuple(int(v) for v in locker['metadata'].get('lock-version', '1.0').split('.'))
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

    def __hashes4file(self, files: List['NameDict']) -> Generator['HashType', None, None]:
        from cyclonedx.exception.model import UnknownHashTypeException
        from cyclonedx.model import HashType

        for file in files:
            if 'hash' in file:
                try:
                    yield HashType.from_composite_str(file['hash'])
                except UnknownHashTypeException as error:
                    self._logger.debug('skipping hash %s', file['hash'], exc_info=error)
                    del error

    __PACKAGE_SRC_VCS = ['git']

    @classmethod
    def __is_package_src_vcs(cls, package: 'NameDict') -> bool:
        return package['source'].get('type') in cls.__PACKAGE_SRC_VCS

    def __make_component4lock(self, package: 'NameDict') -> 'Component':
        from cyclonedx.model import Property
        from cyclonedx.model.component import Component, ComponentScope
        from packageurl import PackageURL

        from . import PropertyName

        return Component(
            bom_ref=f'{package["name"]}@{package["version"]}',
            name=package['name'],
            version=package['version'],
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
                    value=package['source']['reference']
                ) if self.__is_package_src_vcs(package) and 'reference' in package['source'] else None,
                Property(
                    name=PropertyName.PoetryPackageSourceResolvedReference.value,
                    value=package['source']['resolved_reference']
                ) if self.__is_package_src_vcs(package) and 'resolved_reference' in package['source'] else None,
            ]),
            purl=PackageURL(type='pypi', name=package['name'], version=package['version']),
        )

    def __extrefs4lock(self, package: 'NameDict') -> Generator['ExternalReference', None, None]:
        from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
        from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri

        # TODO:
        #   - local deps

        source_type = package['source'].get('type', 'legacy')
        self._logger.debug('ref 4 package files = %r', package['files'])
        if 'legacy' == source_type:
            source_url = package['source'].get('url', 'https://pypi.org/simple')
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
        elif 'url' == source_type:
            try:
                yield ExternalReference(
                    comment='from url',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(package['source']['url']),
                    hashes=[HashType.from_composite_str(package['files'][0]['hash'])] if len(package['files']) else None
                )
            except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
                self._logger.debug('%s skipped dist-extRef for: %r', package['name'], exc_info=error)
                del error
        elif source_type in self.__PACKAGE_SRC_VCS:
            try:
                yield ExternalReference(
                    comment=f'from git (resolved_reference={package["source"].get("resolved_reference")})',
                    type=ExternalReferenceType.VCS,
                    url=XsUri(f'git+{package["source"]["url"]}#{package["source"].get("reference")}')
                    # no hashes, has source.reference instead, which is a property
                )
            except (InvalidUriException, UnknownHashTypeException) as error:  # pragma: nocover
                self._logger.debug('%s skipped dist-extRef for: %r', package['name'], exc_info=error)
                del error
