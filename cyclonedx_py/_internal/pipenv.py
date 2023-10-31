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

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `time -v` for max resident size and see if this changes when global imports are used


class PipenvBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser, FileType

        p = ArgumentParser(description='Build an SBOM based on PipEnv',
                           **kwargs)
        p.add_argument('lock-file',
                       help='I HELP TODO (default: %(default)s)',
                       nargs=OPTIONAL,
                       type=FileType('rb'),
                       default='Pipfile.lock')
        return p

    def __init__(self,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self,  # type:ignore[override]
                 infile: BinaryIO,
                 **kwargs: Any) -> 'Bom':
        from cyclonedx.model.bom import Bom

        if not isinstance(infile, list):
            infile = [infile]
        # TODO
        return Bom()
