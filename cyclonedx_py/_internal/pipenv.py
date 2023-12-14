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


from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Set, Tuple

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model import ExternalReference
    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component, ComponentType

    NameDict = Dict[str, Any]


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class PipenvBB(BomBuilder):
    __LOCKFILE_META = '_meta'

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser
        from os import getenv

        from cyclonedx.model.component import ComponentType

        from .utils.args import argparse_type4enum, arpaese_split

        p = ArgumentParser(description='Build an SBOM from Pipenv',
                           **kwargs)
        # the args shall mimic the ones from Pipenv
        p.add_argument('--categories',
                       metavar='CATEGORIES',
                       dest='categories',
                       type=arpaese_split({' ', ','}),
                       default=[])
        p.add_argument('-d', '--dev',
                       help='both develop and default packages [env var: PIPENV_DEV]',
                       action='store_true',
                       dest='dev',
                       default=bool(getenv('PIPENV_DEV', '')))
        p.add_argument('--pypi-mirror',
                       metavar='URL',
                       help='Specify a PyPI mirror',
                       dest='pypi_url',
                       default='https://pypi.org/simple')
        p.add_argument('--pyproject',
                       metavar='pyproject.toml',
                       help="Path to the root component's `pyproject.toml` according to PEP621",
                       dest='pyproject_file',
                       default=None)
        _mc_types = [ComponentType.APPLICATION,
                     ComponentType.FIRMWARE,
                     ComponentType.LIBRARY]
        p.add_argument('--mc-type',
                       metavar='TYPE',
                       help='Type of the main component'
                            f' {{choices: {", ".join(t.value for t in _mc_types)}}}'
                            ' (default: %(default)s)',
                       dest='mc_type',
                       choices=_mc_types,
                       type=argparse_type4enum(ComponentType),
                       default=ComponentType.APPLICATION.value)
        p.add_argument('project_directory',
                       metavar='project-directory',
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
                 categories: List[str],
                 dev: bool,
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        from json import loads as json_loads
        from os.path import join

        # the group-args shall mimic the ones from Pipenv, which uses (comma and/or space)-separated lists
        # values be like: 'foo bar,bazz' -> ['foo', 'bar', 'bazz']
        lock_groups: Set[str] = set()
        if len(categories) == 0:
            lock_groups.add('default')
            if dev:
                lock_groups.add('develop')
        else:
            lock_groups.update(categories)
            lock_groups.remove(self.__LOCKFILE_META)
            if 'packages' in lock_groups:
                lock_groups.remove('packages')
                lock_groups.add('default')
            if 'dev-packages' in lock_groups:
                lock_groups.remove('dev-packages')
                lock_groups.add('develop')

        lock_file = join(project_directory, 'Pipfile.lock')
        try:
            lock = open(lock_file, 'rt', encoding='utf8', errors='replace')
        except OSError as err:
            raise ValueError(f'Could not open lock file: {lock_file}') from err
        with lock:
            if pyproject_file is None:
                rc = None
            else:
                from .utils.pep621 import pyproject_file2component
                rc = pyproject_file2component(pyproject_file, type=mc_type)
                rc.bom_ref.value = 'root-component'

            return self._make_bom(rc,
                                  json_loads(lock.read()),
                                  lock_groups)

    def _make_bom(self, rc: Optional['Component'], locker: 'NameDict',
                  use_groups: Set[str]
                  ) -> 'Bom':
        from cyclonedx.model import Property
        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL

        from . import PropertyName
        from .utils.bom import make_bom

        self._logger.debug('use_groups: %r', use_groups)

        meta: NameDict = locker[self.__LOCKFILE_META]
        source_urls: Dict[str, str] = dict((source['name'], source['url']) for source in meta.get('sources', []))

        all_components: Dict[str, Component] = {}
        if rc:
            # root for self-installs
            all_components[rc.name] = rc
        for group_name in use_groups:
            for package_name, package_data in locker.get(group_name, {}):
                if package_name in all_components:
                    component = all_components[package_name]
                else:
                    component = all_components[package_name] = Component(
                        bom_ref=f'{package_name}{package_data["version"]}',
                        type=ComponentType.LIBRARY,
                        name=package_name,
                        version=package_data['version'][2:],
                        external_references=self.__make_extrefs(group_name, package_data, source_urls),
                        purl=None  # TODO
                    )
                    component.purl = PackageURL(type='pypi',
                                                name=component.name,
                                                version=component.version,
                                                qualifiers=self.__purl_qualifiers4lock(package_data, source_urls)
                                                ) if not self.__is_local(package_data) else None
                component.properties.add(Property(
                    name=PropertyName.PipenvCategory.value,
                    value=group_name
                ))
                component.properties.update(Property(
                    name=PropertyName.PackageExtra.value,
                    value=package_extra
                ) for package_extra in package_data.get('extras', []))

        bom = make_bom(
            components=(c for c in all_components.values() if c is not rc)
        )
        bom.metadata.component = rc
        return bom

    def __is_local(self, data: 'NameDict') -> bool:
        if 'file' in data:
            location: str = data['file']
        elif 'path' in data:
            location = data['path']
        else:
            return False
        # schema length is expected to be at least 2 chars, to prevent confusion with Windows drive letters `C:\`
        might_have_schema = location.find(':', 2)
        if might_have_schema <= 0:
            return True
        maybe_schema = location[:might_have_schema]
        # example data
        # - file:../MyProject
        # - file:///home/user/projects/MyProject
        # - git+file:///home/user/projects/MyProject
        # - http://acme.org/MyProject/files/foo-bar.tar.gz
        return maybe_schema == 'file' or maybe_schema.endswith('+file')

    __VCS_TYPES = ('git', 'hg', 'svn', 'bzr')
    """ VCS types supported by pip.
        see https://pip.pypa.io/en/latest/topics/vcs-support/#vcs-support
    """

    def __package_vcs(self, data: 'NameDict') -> Optional[Tuple[str, Any]]:
        for vct in self.__VCS_TYPES:
            if vct in data:
                return vct, data[vct]
        return None

    def __make_extrefs(self, name: str, data: 'NameDict', source_urls: Dict[str, str]
                       ) -> Generator['ExternalReference', None, None]:
        from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
        from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri

        hashes = (HashType.from_composite_str(package_hash)
                  for package_hash
                  in data.get('hashes', []))
        vcs_source = self.__package_vcs(data)
        try:
            if vcs_source is not None:
                yield ExternalReference(
                    comment=f'from {vcs_source[0]}',
                    type=ExternalReferenceType.VCS,
                    url=XsUri(f'{vcs_source[1]}#{data.get("ref", "")}'))
            elif 'file' in data:
                yield ExternalReference(
                    comment='from file',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(data['file']),
                    hashes=hashes)
            elif 'path' in data:
                yield ExternalReference(
                    comment='from path',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(data['path']),
                    hashes=hashes)
            elif 'index' in data:
                yield ExternalReference(
                    comment=f'from explicit index: {data["index"]}',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(f'{source_urls[data["index"]]}/{name}/'),
                    hashes=hashes)
            else:
                yield ExternalReference(
                    comment='from implicit index: pypi',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(f'{source_urls["pypi"]}/{name}/'),
                    hashes=hashes)
        except (InvalidUriException, UnknownHashTypeException, KeyError) as error:
            self._logger.debug('skipped dist-extRef for: %r', name, exc_info=error)

    def __purl_qualifiers4lock(self, data: 'NameDict', sourcees: Dict[str, str]) -> 'NameDict':
        # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
        qs = {}
        vcs_source = self.__package_vcs(data)
        if vcs_source is not None:
            # see section 3.7.4 in https://github.com/spdx/spdx-spec/blob/cfa1b9d08903/chapters/3-package-information.md
            # > For version-controlled files, the VCS location syntax is similar to a URL and has the:
            # > `<vcs_tool>+<transport>://<host_name>[/<path_to_repository>][@<revision_tag_or_branch>][#<sub_path>]`
            qs['vcs_url'] = f'{vcs_source[1]}@{data["ref"]}'
        elif 'file' in data:
            if '://files.pythonhosted.org/' not in data['file']:
                # skip PURL bloat, do not add implicit information
                qs['download_url'] = data['file']
        elif 'index' in data:
            source_url = sourcees.get(data['index'], 'https://pypi.org/simple')
            if '://pypi.org/' not in source_url:
                # skip PURL bloat, do not add implicit information
                qs['repository_url'] = source_url
        return qs

    def __make_dependency_graph(self) -> None:
        pass  # TODO: gather info from `pipenv graph --json-tree` and work with it
