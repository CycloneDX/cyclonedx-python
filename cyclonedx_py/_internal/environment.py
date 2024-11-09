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
from importlib.metadata import distributions
from json import loads
from os import getcwd, name as os_name
from os.path import exists, isdir, join
from subprocess import run  # nosec
from sys import path as sys_path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple

from cyclonedx.model import Property
from cyclonedx.model.component import Component, ComponentEvidence, ComponentType
from packageurl import PackageURL
from packaging.requirements import Requirement

from . import BomBuilder, PropertyName, PurlTypePypi
from .cli_common import add_argument_mc_type, add_argument_pyproject
from .utils.cdx import find_LicenseExpression, licenses_fixup, make_bom
from .utils.packaging import metadata2extrefs, metadata2licenses, normalize_packagename
from .utils.pep610 import PackageSourceArchive, PackageSourceVcs, packagesource2extref, packagesource4dist
from .utils.pep639 import dist2licenses as dist2licenses_pep639
from .utils.pyproject import pyproject2component, pyproject2dependencies, pyproject_load

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom

    from .utils.pep610 import PackageSource

    T_AllComponents = Dict[str, Tuple['Component', Iterable[Requirement]]]


class EnvironmentBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(description='Build an SBOM from Python (virtual) environment',
                           **kwargs)
        if os_name == 'nt':
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from python environment:
                       > %(prog)s
                 • Build an SBOM from a Python (virtual) environment:
                       > %(prog)s "...\\some\\path\\bin\\python.exe"
                       > %(prog)s "...\\some\\path\\.venv"
                       > %(prog)s "$env:VIRTUAL_ENV"
                       > %(prog)s %%VIRTUAL_ENV%%
                 • Build an SBOM from specific Python environment:
                       > where.exe python3.9.exe
                       > %(prog)s "%%path-to-specific-python%%"
                 • Build an SBOM from conda Python environment:
                       > conda.exe run where.exe python
                       > %(prog)s "%%path-to-conda-python%%"
                 • Build an SBOM from Pipenv environment:
                       > pipenv.exe --py
                       > pipenv.exe --venv
                       > %(prog)s "%%path-to-pipenv-python%%"
                 • Build an SBOM from Poetry environment:
                       > poetry.exe env info --executable
                       > %(prog)s "%%path-to-poetry-python%%"
                 • Build an SBOM from PDM environment:
                       > pdm.exe info --python
                       > %(prog)s "%%path-to-pdm-python%%"
               """)
        else:  # if os_name == 'posix':
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from python environment:
                       $ %(prog)s
                 • Build an SBOM from a Python (virtual) environment:
                       $ %(prog)s '.../some/path/bin/python'
                       $ %(prog)s '.../some/path/.venv'
                       $ %(prog)s "$VIRTUAL_ENV"
                 • Build an SBOM from specific Python environment:
                       $ %(prog)s "$(which python3.9)"
                 • Build an SBOM from conda Python environment:
                       $ %(prog)s "$(conda run which python)"
                 • Build an SBOM from Pipenv environment:
                       $ %(prog)s "$(pipenv --py)"
                       $ %(prog)s "$(pipenv --venv)"
                 • Build an SBOM from Poetry environment:
                       $ %(prog)s "$(poetry env info --executable)"
                 • Build an SBOM from PDM environment:
                       $ %(prog)s "$(pdm info --python)"
               """)
        p.add_argument('--PEP-639',
                       action='store_true',
                       dest='pep639',
                       help='Enable license gathering according to PEP 639 '
                            '(improving license clarity with better package metadata).\n'
                            'The behavior may change during the draft development of the PEP.')
        p.add_argument('--gather-license-texts',
                       action='store_true',
                       dest='gather_license_texts',
                       help='Enable license text gathering.')
        add_argument_pyproject(p)
        add_argument_mc_type(p)
        # TODO possible additional switch:
        #  `--exclude <package>` Exclude specified package from the output (multi use)
        #  `--local`        If in a virtualenv that has global access, do not list globally-installed packages.
        #  `--user`         Only output packages installed in user-site.
        #  `--path <path>`  Restrict to the specified installation path for listing packages
        p.add_argument('python',
                       metavar='<python>',
                       help='Python interpreter',
                       nargs=OPTIONAL,
                       default=None)
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 pep639: bool,
                 gather_license_texts: bool,
                 **__: Any) -> None:
        self._logger = logger
        self._pep639 = pep639
        self._gather_license_texts = gather_license_texts

    def __call__(self, *,  # type:ignore[override]
                 python: Optional[str],
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        if pyproject_file is None:
            rc = None
        else:
            pyproject = pyproject_load(pyproject_file)
            root_c = pyproject2component(pyproject, ctype=mc_type, fpath=pyproject_file)
            root_c.bom_ref.value = 'root-component'
            root_d = tuple(pyproject2dependencies(pyproject))
            rc = (root_c, root_d)

        path: List[str]
        if python:
            path = self.__path4python(python)
        else:
            path = sys_path.copy()
        if path[0] in ('', getcwd()):
            path.pop(0)

        bom = make_bom()
        self.__add_components(bom, rc, path=path)
        return bom

    def __add_components(self, bom: 'Bom',
                         rc: Optional[Tuple['Component', Iterable['Requirement']]],
                         **kwargs: Any) -> None:
        all_components: 'T_AllComponents' = {}
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
            if self._pep639:
                pep639_licenses = list(dist2licenses_pep639(dist, self._gather_license_texts, self._logger))
                pep639_lexp = find_LicenseExpression(pep639_licenses)
                if pep639_lexp is not None:
                    component.licenses = (pep639_lexp,)  # type:ignore[assignment]
                    pep639_licenses.remove(pep639_lexp)
                if len(pep639_licenses) > 0:
                    if find_LicenseExpression(component.licenses) is None:
                        component.licenses.update(pep639_licenses)
                    else:
                        # hack for preventing expressions AND named licenses.
                        # see https://github.com/CycloneDX/cyclonedx-python/issues/826
                        # see https://github.com/CycloneDX/specification/issues/454
                        component.evidence = ComponentEvidence(licenses=pep639_licenses)
                del pep639_lexp, pep639_licenses

            del dist_meta, dist_name, dist_version
            self.__component_add_extref_and_purl(component, packagesource4dist(dist))
            all_components[normalize_packagename(component.name)] = (
                component,
                tuple(map(Requirement, dist.requires or ()))
            )

            self._logger.info('add component for package %r', component.name)
            self._logger.debug('add component: %r', component)
            bom.components.add(component)

        if rc is not None:
            root_c = rc[0]
            root_c_npname = normalize_packagename(root_c.name)
            root_c_existed = all_components.get(root_c_npname)
            if root_c_existed is not None:
                bom.components.remove(root_c_existed[0])
            del root_c_existed
            all_components[root_c_npname] = rc
            bom.metadata.component = root_c
            self._logger.debug('root-component: %r', root_c)

        self.__finalize_dependencies(bom, all_components)

    def __finalize_dependencies(self, bom: 'Bom', all_components: 'T_AllComponents') -> None:
        for component, requires in all_components.values():
            component_deps: List[Component] = []
            for req in requires:
                req_component: Optional[Component] = all_components.get(normalize_packagename(req.name), (None,))[0]
                if req_component is None:
                    continue
                if req_component is component:
                    # circulars are a typical thing when extras require other extras
                    continue
                component_deps.append(req_component)
                req_component.properties.update(
                    Property(
                        name=PropertyName.PythonPackageExtra.value,
                        value=normalize_packagename(extra)
                    ) for extra in req.extras
                )
            bom.register_dependency(component, component_deps)

    def __component_add_extref_and_purl(self, component: 'Component',
                                        packagesource: Optional['PackageSource']) -> None:
        purl_qs = {}  # https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
        purl_subpath = None
        if packagesource is not None:
            if packagesource.subdirectory:
                component.properties.add(Property(
                    name=PropertyName.PythonPackageSourceSubdirectory.value,
                    value=packagesource.subdirectory))
                purl_subpath = packagesource.subdirectory
            if isinstance(packagesource, PackageSourceVcs):
                purl_qs['vcs_url'] = f'{packagesource.vcs}+{packagesource.url}@{packagesource.commit_id}'
                component.properties.add(Property(
                    name=PropertyName.PythonPackageSourceVcsCommitId.value,
                    value=packagesource.commit_id))
                if packagesource.requested_revision:
                    component.properties.add(Property(
                        name=PropertyName.PythonPackageSourceVcsRequestedRevision.value,
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
            component.purl = PackageURL(
                type=PurlTypePypi,
                name=component.name,
                version=component.version,
                qualifiers=purl_qs,
                subpath=purl_subpath)

    @staticmethod
    def __py_interpreter(value: str) -> str:
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
