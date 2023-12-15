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
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class CondaBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import ArgumentParser

        p = ArgumentParser(description='Build an SBOM from a conda environment',
                           **kwargs)
        # TODO
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **__: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 lock: BinaryIO,
                 **__: Any) -> 'Bom':
        from .utils.bom import make_bom

        bom = make_bom()

        # TODO

        # maybe shell-out (forward all env cars starting with `CONDA_`)
        #
        # see also: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html
        # see also: https://docs.conda.io/projects/conda/en/latest/dev-guide/deep-dives/context.html
        #
        # - `conda list -q [-n ENVIRONMENT] [-p PATH] [--no-pip] [-f] [FILTER]`
        #   - `conda list --json`
        #   - `conda list --export --explicit --md5`
        # - `conda info`

        # maybe have an own conda command/plugin?
        # see https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/conda-plugins.html

        # maybe create a executable `conda-cyclonedx`
        # if it is in the shell path, conda will pick it up and have it made available via `conda cyclonedx`
        # and it will add some env vars:
        # - CONDA_ROOT

        return bom
