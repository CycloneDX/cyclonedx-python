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


class EnvironmentBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import ArgumentParser

        p = ArgumentParser(description='Build an SBOM based on python environment',
                           **kwargs)
        # TODO
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 lock: BinaryIO,
                 **kwargs: Any) -> 'Bom':
        from .utils.bom import make_bom

        bom = make_bom()

        # TODO
        # maybe utilize https://github.com/tox-dev/pipdeptree ?

        return bom
