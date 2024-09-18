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
from json import loads as json_loads
from os import getenv
from os.path import join
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, Generator, List, Optional, Set, Tuple

from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
from cyclonedx.model.component import Component, ComponentType
from packageurl import PackageURL

from . import BomBuilder, PropertyName, PurlTypePypi
from .cli_common import add_argument_mc_type, add_argument_pyproject
from .utils.args import arparse_split
from .utils.cdx import make_bom
from .utils.packaging import normalize_packagename
from .utils.pyproject import pyproject_file2component
from .utils.secret import redact_auth_from_url

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom

    NameDict = Dict[str, Any]


class PipenvBB(BomBuilder):
    __LOCKFILE_META = '_meta'

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(description=dedent("""\
                           Build an SBOM from Pipenv manifest.

                           The options and switches mimic the respective ones from Pipenv CLI.
                           """),
                           **kwargs)
        # the options and switches SHALL mimic the ones from Pipenv
        # see also: https://pipenv.pypa.io/en/latest/configuration.html
        p.add_argument('--categories',
                       # help='', # Pipenv had no help for this, so I guess its okay...
                       metavar='<categories>',
                       dest='categories',
                       type=arparse_split(' ', ','),
                       default=[])
        p.add_argument('-d', '--dev',
                       help='Analyse both develop and default packages'
                            ' [env var: PIPENV_DEV]',
                       action='store_true',
                       dest='dev',
                       default=getenv('PIPENV_DEV', '').lower() in ('1', 'true', 'yes', 'on'))
        p.add_argument('--pypi-mirror',
                       metavar='<url>',
                       help='Specify a PyPI mirror'
                            ' [env var: PIPENV_PYPI_MIRROR]',
                       dest='pypi_url',
                       default=getenv('PIPENV_PYPI_MIRROR'))
        add_argument_pyproject(p)
        add_argument_mc_type(p)
        p.add_argument('project_directory',
                       metavar='<project-directory>',
                       help='The project directory for Pipenv'
                            ' (default: current working directory)\n'
                            'Unlike Pipenv tool, there is no search-up in this very tool. '  # yet
                            'Please provide the actual directory that contains `Pipfile` and `Pipfile.lock` file.',
                       nargs=OPTIONAL,
                       default='.')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 pypi_url: Optional[str],
                 **__: Any) -> None:
        self._logger = logger
        self._pypi_url = pypi_url or None  # ignore empty strings

    def __call__(self, *,  # type:ignore[override]
                 project_directory: str,
                 categories: List[str],
                 dev: bool,
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':

        # the group-args shall mimic the ones from Pipenv, which uses (comma and/or space)-separated lists
        # values be like: 'foo bar,bazz' -> ['foo', 'bar', 'bazz']
        lock_groups: Set[str] = set()
        if len(categories) == 0:
            lock_groups.add('default')
            if dev:
                lock_groups.add('develop')
        else:
            lock_groups.update(categories)
            lock_groups.discard(self.__LOCKFILE_META)
            if 'packages' in lock_groups:
                # replace UI-category with Lock-group
                lock_groups.remove('packages')
                lock_groups.add('default')
            if 'dev-packages' in lock_groups:
                # replace UI-category with Lock-group
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
                rc = pyproject_file2component(pyproject_file, ctype=mc_type)
                rc.bom_ref.value = 'root-component'

            return self._make_bom(rc,
                                  json_loads(lock.read()),
                                  frozenset(lock_groups))

    def _make_bom(self, root_c: Optional['Component'],
                  locker: 'NameDict', use_groups: FrozenSet[str]) -> 'Bom':
        self._logger.debug('use_groups: %r', use_groups)

        bom = make_bom()
        bom.metadata.component = root_c
        self._logger.debug('root-component: %r', root_c)

        meta: NameDict = locker[self.__LOCKFILE_META]
        source_urls: Dict[str, str] = {
            source['name']: redact_auth_from_url(source['url']).rstrip('/')
            for source in meta.get('sources', ())
        }
        if self._pypi_url is not None:
            source_urls['pypi'] = redact_auth_from_url(self._pypi_url).rstrip('/')

        all_components: Dict[str, Component] = {}
        if root_c:
            # root for possible self-installs
            all_components[normalize_packagename(root_c.name)] = root_c
        for group_name in use_groups:
            self._logger.debug('processing group %r ...', group_name)
            for package_name, package_data in locker.get(group_name, {}).items():
                package_name_normalized = normalize_packagename(package_name)
                if package_name_normalized in all_components:
                    component = all_components[package_name_normalized]
                    self._logger.info('existing component for package %r', package_name)
                else:
                    component = all_components[package_name_normalized] = Component(
                        bom_ref=f'{package_name}{package_data.get("version", "")}',
                        type=ComponentType.LIBRARY,
                        name=package_name,
                        version=package_data['version'][2:] if 'version' in package_data else None,
                        external_references=self.__make_extrefs(package_name, package_data, source_urls),
                    )
                    component.purl = PackageURL(
                        type=PurlTypePypi,
                        name=component.name,
                        version=component.version,
                        qualifiers=self.__purl_qualifiers4lock(package_data, source_urls)
                    ) if not self.__is_local(package_data) else None
                    self._logger.info('add component for package %r', package_name)
                    self._logger.debug('add component: %r', component)
                    bom.components.add(component)
                component.properties.add(Property(
                    name=PropertyName.PipenvCategory.value,
                    value=group_name
                ))
                component.properties.update(
                    Property(
                        name=PropertyName.PythonPackageExtra.value,
                        value=normalize_packagename(package_extra)
                    ) for package_extra in package_data.get('extras', ())
                )

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

    def __package_vcs(self, data: 'NameDict') -> Optional[Tuple[str, str]]:
        for vct in self.__VCS_TYPES:
            if vct in data:
                url: str = data[vct]
                hash_pos = url.find('#')
                # remove install-annotations, which are behind a `#`
                return vct, url[:hash_pos] if hash_pos >= 0 else url
        return None

    def __make_extrefs(self, name: str, data: 'NameDict', source_urls: Dict[str, str]
                       ) -> Generator['ExternalReference', None, None]:
        hashes = (HashType.from_composite_str(package_hash)
                  for package_hash
                  in data.get('hashes', ()))
        vcs_source = self.__package_vcs(data)
        try:
            if vcs_source is not None:
                vcs_source_url = redact_auth_from_url(vcs_source[1])
                yield ExternalReference(
                    comment=f'from {vcs_source[0]}',
                    type=ExternalReferenceType.VCS,
                    url=XsUri(f'{vcs_source_url}#{data.get("ref", "")}'))
            elif 'file' in data:
                yield ExternalReference(
                    comment='from file',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(redact_auth_from_url(data['file'])),
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
        except (InvalidUriException, UnknownHashTypeException, KeyError) as error:  # pragma: nocover
            self._logger.debug('skipped dist-extRef for: %r', name, exc_info=error)

    def __purl_qualifiers4lock(self, data: 'NameDict', sourcees: Dict[str, str]) -> 'NameDict':
        # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
        qs = {}
        vcs_source = self.__package_vcs(data)
        if vcs_source is not None:
            # see section 3.7.4 in https://github.com/spdx/spdx-spec/blob/cfa1b9d08903/chapters/3-package-information.md
            # > For version-controlled files, the VCS location syntax is similar to a URL and has the:
            # > `<vcs_tool>+<transport>://<host_name>[/<path_to_repository>][@<revision_tag_or_branch>][#<sub_path>]`
            qs['vcs_url'] = f'{redact_auth_from_url(vcs_source[1])}@{data["ref"]}'
        elif 'file' in data:
            if '://files.pythonhosted.org/' not in data['file']:
                # skip PURL bloat, do not add implicit information
                qs['download_url'] = redact_auth_from_url(data['file'])
        elif 'index' in data:
            source_url = sourcees.get(data['index'], 'https://pypi.org/simple')
            if '://pypi.org/' not in source_url:
                # skip PURL bloat, do not add implicit information
                qs['repository_url'] = redact_auth_from_url(source_url.rstrip('/'))
        return qs

    def __make_dependency_graph(self) -> None:
        # possible solution:: gather info from `pipenv graph --json-tree` and work with it
        pass
