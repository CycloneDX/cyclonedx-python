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


from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component, ComponentType

    NameDict = Dict[str, Any]

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
        # the args shall mimic the ones from Pipenv
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
        from .utils.bom import make_bom

        self._logger.debug('use_groups: %r', use_groups)

        bom = make_bom()
        bom.metadata.component = rc
        # TODO: gather info from lock

        return bom

    def __make_dependency_graph(self) -> None:
        pass  # TODO: gather info from `pipenv graph --json-tree` and work with it
