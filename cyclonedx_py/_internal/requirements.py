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


from typing import TYPE_CHECKING, Any, BinaryIO

from . import BomBuilder

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `time -v` for max resident size and see if this changes when global imports are used


class RequirementsBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser, FileType
        from textwrap import dedent

        p = ArgumentParser(description='Build an SBOM from frozen requirements.',
                           epilog=dedent('''\
                           Example Usage:
                             • Build an SBOM from a frozen requirements file:
                                   $ %(prog)s requirements-prod.txt
                             • Merge multiple files and build an SBOM from it:
                                   $ cat requirements/*.txt | %(prog)s -
                             • Build an inventory for all installed packages:
                                   $ python3 -m pip freeze --all | %(prog)s -
                             • Build an inventory from an unfrozen manifest:
                                   $ python3 -m pip install -r dependencies.txt && \\
                                     python3 -m pip freeze | %(prog)s -
                           '''),
                           **kwargs)
        p.add_argument('infile',
                       help='I HELP TODO (default: %(default)s)',
                       nargs=OPTIONAL,
                       type=FileType('rb'),
                       default='requirements.txt')
        return p

    def __init__(self,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self,  # type:ignore[override]
                 infile: BinaryIO,
                 **kwargs: Any) -> 'Bom':
        from cyclonedx.model.bom import Bom

        # TODO

        return Bom()
