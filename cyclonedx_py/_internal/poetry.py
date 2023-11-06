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


import re
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, Generator, List, TextIO, Set, NamedTuple, Iterable, Optional

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model import HashType
    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component

    NameDict = Dict[str, Any]


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `time -v` for max resident size and see if this changes when global imports are used


class _CdxProperty(Enum):
    PackageGroup = 'cdx:poetry:package:group'


class PoetryBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import ArgumentParser, ONE_OR_MORE, OPTIONAL
        from cyclonedx.model.component import ComponentType
        from .utils.args import argparse_type4enum

        p = ArgumentParser(description='Build an SBOM based on Poetry project.',
                           **kwargs)
        # the args shall mimic the ones from poetry
        p.add_argument('--without',
                       metavar='GROUP',
                       dest='groups_without',
                       help='The dependency groups to ignore (multiple values allowed)',
                       action='append',
                       nargs=ONE_OR_MORE,
                       default=[])
        p.add_argument('--with',
                       metavar='GROUP',
                       dest='groups_with',
                       help='The optional dependency groups to include (multiple values allowed)',
                       action='append',
                       nargs=ONE_OR_MORE,
                       default=[])
        p.add_argument('--only',
                       metavar='GROUP',
                       dest='groups_only',
                       help='The only dependency groups to include (multiple values allowed)',
                       action='append',
                       nargs=ONE_OR_MORE,
                       default=[])
        p.add_argument('--no-dev',
                       dest='groups_only',
                       help='Alias for --only=main',
                       action='append_const',
                       const='main')
        eg = p.add_mutually_exclusive_group()
        eg.add_argument('--extras',
                        metavar='EXTRAS',
                        help='Extra sets of dependencies to include (multiple values allowed)',
                        nargs=ONE_OR_MORE,
                        dest='extras',
                        default=False)
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
                 extras: List[str], all_extras: bool,
                 **kwargs: Any) -> 'Bom':
        from os.path import join
        import sys
        if sys.version_info < (3, 11):
            from toml import loads as toml_loads
        else:
            from tomllib import loads as toml_loads

        pyproject_file = join(project_directory, 'pyproject.toml')
        lock_file = join(project_directory, 'poetry.lock')
        try:
            pyproject = open(pyproject_file, 'rt', errors='replace')
        except OSError as err:
            raise ValueError(f"can't open {pyproject_file!r}: {err}")
        try:
            lock = open(lock_file, 'rt', errors='replace')
        except OSError as err:
            pyproject.close()
            raise ValueError(f"can't open {lock_file!r}: {err}")

        with pyproject, lock:
            project = toml_loads(pyproject.read())
            po_cfg = project['tool']['poetry']
            return self._make_bom(
                project, toml_loads(lock.read()),
                po_cfg.get('extras', {}).keys() if all_extras else extras,
            )

    class _LockEntry(NamedTuple):
        name: str
        component: 'Component'
        dependencies: Set[str]
        extras: Dict[str, Set[str]]

    def _make_bom(self, project: 'NameDict', locker: 'NameDict',
                  filter_extras: List[str]
                  ) -> 'Bom':
        from cyclonedx.model import Property

        from .utils.bom import make_bom

        bom = make_bom()

        po_cfg = project['tool']['poetry']

        bom.metadata.component = root_c = self.__component4poetryproj(po_cfg)
        lock_data: Dict[str, self._LockEntry] = {le.name: le for le in self._parse_lock(locker)}

        dep_groups = {None: po_cfg.get('dependencies', {})}
        extra_deps = set(chain.from_iterable(
            eds for en, eds in po_cfg.get('extras', {}).items() if en in filter_extras))
        # TODO add more groups / dev-foo

        _dep_pattern = re.compile(r'^(?P<name>.+?)(?:\[(?P<extras>.*?)\]])?$')

        def _add_ld(name: str, extras: Iterable[str]) -> Optional['Component']:
            if name == 'python':
                return None
            le = lock_data.get(name)
            if le is None:
                self._logger.debug('skip unlocked component: %s', name)
                return None
            if le.component in bom.components:
                self._logger.debug('skipped existing component: %s', name)
                return None
            self._logger.debug('add component: %r', le.component)
            bom.components.add(le.component)
            depends_on = []
            for dep in chain(
                le.dependencies,
                chain.from_iterable(le.extras.get(extra, []) for extra in extras)
            ):
                self._logger.debug('component %s depends on %s', name, dep)
                depm = _dep_pattern.match(dep)
                depends_on.append(_add_ld(
                    depm.group('name'),
                    set(map(str.strip, (depm.group('extras') or '').split(',')))
                ))
            bom.register_dependency(le.component, filter(None, depends_on))
            return le.component

        depends_on = []
        for group_name, group_deps in dep_groups.items():
            for dep_name, dep_spec in group_deps.items():
                dep_spec = dep_spec if isinstance(dep_spec, dict) else {'version': dep_spec}
                if dep_spec.get('optional', False) and dep_name not in extra_deps:
                    self._logger.debug('skip optional dependency: %s', dep_name)
                    continue
                added_c = _add_ld(dep_name, dep_spec.get('extras') or [])
                if added_c is None:
                    continue
                if group_name is not None:
                    added_c.properties.add(Property(
                        name=_CdxProperty.PackageGroup.value,
                        value=group_name
                    ))
                depends_on.append(added_c)
        bom.register_dependency(root_c, filter(None, depends_on))

        return bom

    def __component4poetryproj(self, po_cfg: 'NameDict') -> 'Component':
        from cyclonedx.factory.license import LicenseFactory
        from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri, InvalidUriException
        from cyclonedx.model.component import Component, ComponentType

        # see spec: https://python-poetry.org/docs/pyproject/
        comp = Component(
            bom_ref=str(po_cfg.get('name', 'root-component')),
            type=ComponentType.APPLICATION,  # TODO configurable,
            name=str(po_cfg.get('name', 'unnamed')),
            version=str(po_cfg.get('version', '')) or None,
            description=str(po_cfg.get('description', '')) or None,
            licenses=[LicenseFactory().make_from_string(po_cfg['license'])] if 'license' in po_cfg else None,
            author='; '.join(po_cfg['authors']) if 'authors' in po_cfg else None,
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

        metavar_files = locker['metavar'].get('files', {}) if lock_version < (2,) else {}

        package: 'NameDict'
        for package in locker['package']:
            package.setdefault('files', metavar_files.get(package['name'], []))
            yield self._LockEntry(
                package['name'],
                self.__make_component4lock(package),
                set(package.get('dependencies', {}).keys()),
                {e: set(d.split(' ')[0] for d in ds) for e, ds in package.get('extras', {}).items()}
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

    def __make_component4lock(self, package: 'NameDict') -> 'Component':
        # TODO:
        #   - local deps
        #   - private package
        #   - from urls: wheel, soure-archive, vcs-tag, vcs-commit, vcs-branch

        from cyclonedx.exception.model import InvalidUriException
        from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
        from cyclonedx.model.component import Component, ComponentScope
        from packageurl import PackageURL

        component = Component(
            bom_ref=f'{package["name"]}@{package["version"]}',
            name=package['name'],
            version=package['version'],
            description=package.get('description'),
            scope=ComponentScope.OPTIONAL if package.get('optional') else None,
            properties=filter(None, [
                Property(  # for backwards compatibility: category -> group
                    name=_CdxProperty.PackageGroup.value,
                    value=package['category']
                ) if 'category' in package else None
            ]),
            purl=PackageURL(type='pypi', name=package['name'], version=package['version']),
        )
        """TODO
        fles and hashes eixts, regardless of the source ...
        need to incorporate proper with URL/local files/ etc ...

        package_host = 'https://files.pythonhosted.org'
        for file in package.get('files', []):
            try:
                'hash' in file and component.external_references.add(ExternalReference(
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(
                        # see https://warehouse.pypa.io/api-reference/integration-guide.html#predictable-urls
                        f'{package_host}/packages/source/{component.name[0]}/{component.name}/{file["file"]}'),
                    hashes=[HashType.from_composite_str(file["hash"])]
                ))
            except InvalidUriException as error:
                self._logger.debug('%s skipped extRef for: %r', package['name'], file, exc_info=error)
                del error
        """
        return component
