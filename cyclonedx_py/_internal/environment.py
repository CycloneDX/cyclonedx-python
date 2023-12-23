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


from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component, ComponentType
    from packaging.requirements import Requirement


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class EnvironmentBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser
        from os import name as os_name
        from textwrap import dedent

        from .cli_common import add_argument_mc_type, add_argument_pyproject

        p = ArgumentParser(description='Build an SBOM from Python (virtual) environment',
                           **kwargs)
        if os_name == 'nt':
            # TODO the Windows help-page might need improvement.
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from current python environment:
                       > %(prog)s
                 • Build an SBOM from a Python (virtual) environment:
                       > %(prog)s "...some\\path\\bin\\python.exe"
                       > %(prog)s '...some\\path\\.venv\\'
                 • Build an SBOM from specific Python environment:
                       > where.exe python3.9.exe
                       > %(prog)s "%%path to specific python%%"
                 • Build an SBOM from conda Python environment:
                       > conda run where python
                       > %(prog)s "%%path to conda python%%"
                 • Build an SBOM from Pipenv environment:
                       > pipenv.exe --py
                       > pipenv.exe --venv
                       > %(prog)s "%%path to pipenv python%%"
                 • Build an SBOM from Poetry environment:
                       > poetry.exe env info  --executable
                       > %(prog)s "%%path to poetry python%%"
               """)
        else:  # if os_name == 'posix':
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from current python environment:
                       $ %(prog)s
                 • Build an SBOM from a Python (virtual) environment:
                       $ %(prog)s '...some/path/bin/python'
                       $ %(prog)s '.../.venv/'
                 • Build an SBOM from specific Python environment:
                       $ %(prog)s "$(which python3.9)"
                 • Build an SBOM from conda Python environment:
                       $ %(prog)s "$(conda run which python)"
                 • Build an SBOM from Pipenv environment:
                       $ %(prog)s "$(pipenv --py)"
                       $ %(prog)s "$(pipenv --venv)"
                 • Build an SBOM from Poetry environment:
                       $ %(prog)s "$(poetry env info --executable)"
               """)
        add_argument_pyproject(p)
        add_argument_mc_type(p)
        # TODO possible additional switch:
        #  `--exclude <package>` Exclude specified package from the output (multi use)
        #  `--local`        If in a virtualenv that has global access, do not list globally-installed packages.
        #  `--user`         Only output packages installed in user-site.
        #  `--path <path>`  Restrict to the specified installation path for listing packages
        p.add_argument('python',
                       metavar='python',
                       help='Python interpreter',
                       nargs=OPTIONAL,
                       default=None)
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **__: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 python: Optional[str],
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        from os import getcwd

        from .utils.cdx import make_bom
        from .utils.pyproject import pyproject2dependencies

        if pyproject_file is None:
            rc = None
        else:
            from .utils.pyproject import pyproject2component, pyproject_load
            pyproject = pyproject_load(pyproject_file)
            root_c = pyproject2component(pyproject, type=mc_type)
            root_c.bom_ref.value = 'root-component'
            root_d = pyproject2dependencies(pyproject)
            rc = (root_c, root_d)

        path: List[str]
        if python:
            path = self.__path4python(python)
        else:
            from sys import path as sys_path
            path = sys_path.copy()
        if path[0] in ('', getcwd()):
            path.pop(0)

        bom = make_bom()
        self.__add_components(bom, rc, path=path)
        return bom

    def __add_components(self, bom: 'Bom',
                         rc: Optional[Tuple['Component', Iterable['Requirement']]],
                         **kwargs: Any) -> None:
        from importlib.metadata import distributions

        from cyclonedx.model import Property
        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL
        from packaging.requirements import Requirement

        from . import PropertyName
        from .utils.cdx import licenses_fixup
        from .utils.packaging import metadata2extrefs, metadata2licenses
        from .utils.pep610 import PackageSourceArchive, PackageSourceVcs, packagesource2extref, packagesource4dist

        all_components: Dict[str, Tuple['Component', Iterable[Requirement]]] = {}
        self._logger.debug('distribution context args: %r', kwargs)
        self._logger.info('discovering distributions...')
        for dist in distributions(**kwargs):
            dist_meta = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
            dist_name = dist_meta['Name']
            dist_version = dist_meta['Version']
            component = Component(
                type=ComponentType.LIBRARY,
                bom_ref=f'{dist_name}=={dist_version}',
                name=dist_name,
                version=dist_version,
                description=dist_meta['Summary'] if 'Summary' in dist_meta else None,
                licenses=licenses_fixup(metadata2licenses(dist_meta)),
                external_references=metadata2extrefs(dist_meta),
                # path of dist-package on disc? naaa... a package may have multiple files/folders on disc
            )
            packagesource = packagesource4dist(dist)
            purl_qs = {}  # https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
            purl_subpath = None
            if packagesource is not None:
                if packagesource.subdirectory:
                    component.properties.add(Property(name=PropertyName.PackageSourceSubdirectory.value,
                                                      value=packagesource.subdirectory))
                    purl_subpath = packagesource.subdirectory
                if isinstance(packagesource, PackageSourceVcs):
                    purl_qs['vcs_url'] = f'{packagesource.vcs}+{packagesource.url}@{packagesource.commit_id}'
                    component.properties.add(Property(name=PropertyName.PackageSourceVcsCommitId.value,
                                                      value=packagesource.commit_id))
                    if packagesource.requested_revision:
                        component.properties.add(Property(name=PropertyName.PackageSourceVcsRequestedRevision.value,
                                                          value=packagesource.requested_revision))
                elif isinstance(packagesource, PackageSourceArchive):
                    if '://files.pythonhosted.org/' not in packagesource.url:
                        # skip PURL bloat, do not add implicit information
                        purl_qs['download_url'] = packagesource.url
                packagesource_extref = packagesource2extref(packagesource)
                if packagesource_extref is not None:
                    component.external_references.add(packagesource_extref)
                del packagesource_extref
            if packagesource is None or not packagesource.url.startswith('file://'):
                # no purl for locals and unpublished packages
                component.purl = PackageURL('pypi', name=dist_name, version=dist_version,
                                            qualifiers=purl_qs, subpath=purl_subpath)
            del dist_meta, dist_name, dist_version, packagesource, purl_qs

            all_components[component.name.lower()] = component, map(Requirement, dist.requires or ())

            self._logger.info('add component for package %r', component.name)
            self._logger.debug('add component: %r', component)
            bom.components.add(component)

        if rc is not None:
            root_c = rc[0]
            root_c_lcname = root_c.name.lower()
            root_c_existed = all_components.get(root_c_lcname)
            if root_c_existed is not None:
                bom.components.remove(root_c_existed[0])
                del root_c_existed
            all_components[root_c_lcname] = rc
            bom.metadata.component = root_c

        for component, requires in all_components.values():
            # we know a lot of dependencies, but here we are only interested in those that are actually installed/found
            requires_d: Iterable[Component] = filter(None,
                                                     map(lambda r: all_components.get(r.name.lower(), (None,))[0],
                                                         requires))
            bom.register_dependency(component, requires_d)

    @staticmethod
    def __py_interpreter(value: str) -> str:
        from os.path import exists, isdir, join
        if not exists(value):
            raise ValueError(f'No such file or directory: {value}')
        if isdir(value):
            for venv_loc in (
                ('bin', 'python'),  # unix
                ('Scripts', 'python.exe'),  # win
            ):
                maybe = join(value, *venv_loc)
                if exists(maybe):
                    return maybe
            raise ValueError(f'Failed to find python in directory: {value}')
        return value

    def __path4python(self, python: str) -> List[str]:
        from json import loads
        from subprocess import run  # nosec
        cmd = self.__py_interpreter(python), '-c', 'import json,sys;json.dump(sys.path,sys.stdout)'
        self._logger.debug('fetch `path` from python interpreter cmd: %r', cmd)
        res = run(cmd, capture_output=True, encoding='utf8', shell=False)  # nosec
        if res.returncode != 0:
            raise RuntimeError('Fail fetching `path` from Python interpreter.\n'
                               f'returncode: {res.returncode}\n'
                               f'stdout: {res.stdout}\n'
                               f'stderr: {res.stderr}\n')
        self._logger.debug('got `path` from Python interpreter: %r', res.stdout)
        return loads(res.stdout)  # type:ignore[no-any-return]
