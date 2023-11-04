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


from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, TextIO, Tuple

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
        from argparse import OPTIONAL, ArgumentParser

        p = ArgumentParser(description='Build an SBOM based on Poetry environment.',
                           **kwargs)
        p.add_argument('lock_file',
                       metavar='lock-file',
                       help='I HELP TODO (default: %(default)s)',
                       nargs=OPTIONAL,
                       default='poetry.lock')
        # TODO: filtering as allowed by poetry itself
        #  --without=GROUP     The dependency groups to ignore. (multiple values allowed)
        #  --with=GROUP        The optional dependency groups to include. (multiple values allowed)
        #  --only=GROUP        The only dependency groups to include. (multiple values allowed)
        #  --dev / --no-dev    ala: Do not install the development dependencies.
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 lock_file: str,
                 **kwargs: Any) -> 'Bom':

        try:
            lock = open(lock_file, 'rt', errors='replace')
        except OSError as err:
            raise ValueError(f"can't open {lock_file!r}: {err}")

        with lock:
            return self._make_bom(lock)

    def _make_bom(self, lock: TextIO) -> 'Bom':
        import sys

        if sys.version_info < (3, 11):
            from toml import loads as toml_loads
        else:
            from tomllib import loads as toml_loads

        locker = toml_loads(lock.read())
        lock_version = self.__get_lock_version(locker)
        self._logger.debug('lock_version: %r', lock_version)

        if lock_version >= (2, 0):
            return self._make_bom_v2(locker)
        return self._make_bom_v1(locker)

    @staticmethod
    def __get_lock_version(locker: 'NameDict') -> Tuple[int, ...]:
        # no version defined -- assume 1.0
        return tuple(int(v) for v in locker['metadata'].get('lock-version', '1.0').split('.'))

    def __hashes4file(self, files: List['NameDict']) -> Generator['HashType', None, None]:
        from cyclonedx.exception.model import UnknownHashTypeException
        from cyclonedx.model import HashType

        for file in files:
            if 'hash' in file:
                try:
                    yield HashType.from_composite_str(file['hash'])
                except UnknownHashTypeException:
                    pass

    def __make_component(self, package: 'NameDict', files: List['NameDict']) -> 'Component':
        from cyclonedx.model import Property, XsUri, ExternalReference, ExternalReferenceType, HashType
        from cyclonedx.exception.model import InvalidUriException
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
                # TODO actual groups -- from `pyproject.toml`
            ]),
            purl=PackageURL(type='pypi', name=package['name'], version=package['version']),
        )
        for file in files:
            try:
                'hash' in file and component.external_references.add(ExternalReference(
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(component.get_pypi_url()),
                    comment=f'file: {file["file"]}',
                    hashes=[HashType.from_composite_str(file["hash"])]
                ))
            except InvalidUriException as error:
                self._logger.debug(f'%s skipped file: %r', package['name'], file, exc_info=error)
        return component

    def _make_bom_v1(self, lock: 'NameDict') -> 'Bom':
        from cyclonedx.model.bom import Bom

        metavar_files = lock.get('metavar', {}).get('files', {})

        bom = Bom()

        for package in lock.get('package', []):
            component = self.__make_component(package, metavar_files.get(package['name'], []))
            self._logger.debug('Add component: %r', component)
            bom.components.add(component)

        # TODO dependency tree

        return bom

    def _make_bom_v2(self, lock: 'NameDict') -> 'Bom':
        from cyclonedx.model.bom import Bom

        bom = Bom()

        for package in lock.get('package', []):
            component = self.__make_component(package, package.get('files', []))
            self._logger.debug('Add component: %r', component)
            bom.components.add(component)

        # TODO dependency tree

        return bom
