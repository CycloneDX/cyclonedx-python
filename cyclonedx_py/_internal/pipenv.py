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


from typing import TYPE_CHECKING, Any, Iterable, Optional, Set

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import ComponentType


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class PipenvBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser
        from os import getenv

        from .utils.args import argparse_type4enum, arpaese_split

        p = ArgumentParser(description='Build an SBOM from Pipenv',
                           **kwargs)
        p.add_argument('--categories',
                       metavar='CATEGORIES',
                       dest='categories',
                       type=arpaese_split({' ', ','}),
                       default=[])
        p.add_argument('-d', '--dev',
                       help='both develop and default packages [env var: PIPENV_DEV]',
                       action='store-true',
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
                 categories: Iterable[str],
                 dev: bool,
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        from .utils.bom import make_bom

        groups: Set[str] = {'packages', *categories}
        if dev:
            groups.add('dev-packages')

        bom = make_bom()
        # TODO: gather info from lock
        # TODO: gather info from pyproject_file

        return bom

    def __make_dependency_graph(self) -> None:
        pass  # TODO: gather info from `pipenv graph --json-tree` and work with it
