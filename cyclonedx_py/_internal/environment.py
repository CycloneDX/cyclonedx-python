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

from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Tuple

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component, ComponentType


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class EnvironmentBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser
        from textwrap import dedent
        from os import name as os_name

        from cyclonedx.model.component import ComponentType

        from .utils.args import argparse_type4enum

        p = ArgumentParser(description='Build an SBOM from Python (virtual) environment',
                           **kwargs)
        if os_name == 'nt':
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from current python environment:
                       > %(prog)s
                 • Build an SBOM from a (virtual) python environment:
                       > %(prog)s "...\\bin\\python.exe"
                 • Build an SBOM from a specific python environment:
                       > where.exe python3.9.exe
                       > %(prog)s "%%path to specific python%%"
                 • Build an SBOM from conda python environment:
                       > conda run where python
                       > %(prog)s "%%path to conda python%%"
                 • Build an SBOM from Pipenv virtual python environment:
                       > pipenv.exe --py
                       > %(prog)s "%%path to pipenv python%%"
                 • Build an SBOM from Poetry virtual python environment:
                       > poetry.exe env info -e
                       > %(prog)s "%%path to poetry python%%"
               """)
        else:  # if os_name == 'posix':
            p.epilog = dedent("""\
               Example Usage:
                 • Build an SBOM from current python environment:
                       $ %(prog)s
                 • Build an SBOM from a (virtual) python environment:
                       $ %(prog)s '.../bin/python'
                 • Build an SBOM from a specific python environment:
                       $ %(prog)s "$(which python3.9)"
                 • Build an SBOM from conda python environment:
                       $ %(prog)s "$(conda run which python)"
                 • Build an SBOM from Pipenv virtual python environment:
                       $ %(prog)s "$(pipenv --py)"
                 • Build an SBOM from Poetry virtual python environment:
                       $ %(prog)s "$(poetry env info -e)"
               """)
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
                       default=ComponentType.APPLICATION)
        p.add_argument('python',
                       metavar='python',
                       help='I HELP TODO',
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
        from .utils.cdx import make_bom

        if pyproject_file is None:
            rc = None
        else:
            from .utils.pep621 import pyproject2component, pyproject_dependencies, pyproject_load
            from .utils.pep631 import requirement2package_name
            pyproject = pyproject_load(pyproject_file)
            root_c = pyproject2component(pyproject, type=mc_type)
            root_c.bom_ref.value = 'root-component'
            root_d = set(filter(None, map(requirement2package_name, pyproject_dependencies(pyproject))))
            rc = (root_c, root_d)

        path: List[str]
        if python:
            path = self.__path4python(python)
        else:
            from sys import path as sys_path
            path = sys_path

        bom = make_bom()
        self.__add_components(bom, rc, path=path)
        return bom

    def __add_components(self, bom: 'Bom', rc: Optional[Tuple['Component', Set[str]]],
                         **kwargs: Any) -> None:
        from importlib.metadata import distributions

        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL

        from .utils.cdx import licenses_fixup
        from .utils.packaging import metadata2extrefs, metadata2licenses
        from .utils.pep631 import requirement2package_name

        all_components: Dict[str, Tuple['Component', Set[str]]] = {}
        self._logger.debug('distribution context args: %r', kwargs)
        self._logger.info('discovering distributions...')
        for dist in distributions(**kwargs):
            dist_meta = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
            dist_name = dist_meta['Name']
            dist_version = dist_meta['Version']
            # print(repr(dist_meta.items()))
            component = Component(
                type=ComponentType.LIBRARY,
                bom_ref=f'{dist_name}=={dist_version}',
                name=dist_name,
                version=dist_version,
                description=dist_meta['Summary'] if 'Summary' in dist_meta else None,
                licenses=licenses_fixup(metadata2licenses(dist_meta)),
                external_references=metadata2extrefs(dist_meta),
                purl=PackageURL('pypi', name=dist_name, version=dist_version),
                # TODO install info
                # TODO path of package?
            )
            del dist_meta, dist_name, dist_version
            all_components[component.name.lower()] = (
                component,
                set(filter(None, map(requirement2package_name, dist.requires or ())))
            )
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
                                                     map(lambda r: all_components.get(r, (None,))[0],
                                                         requires))
            bom.register_dependency(component, requires_d)

    def __path4python(self, python: str) -> List[str]:
        from json import loads
        from subprocess import run
        cmd = python, '-c', 'import json,sys;json.dump(sys.path,sys.stdout)'
        self._logger.debug('fetch `path` from python interpreter cmd: %r', cmd)
        res = run(cmd, capture_output=True, encoding='utf8', shell=False)
        if res.returncode != 0:
            raise ValueError(f'Fail fetching `path` from python: {res.stderr}')
        self._logger.debug('got `path` from python interpreter: %r', res.stdout)
        return loads(res.stdout)  # type:ignore[no-any-return]
