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


from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom


class BomBuilder(ABC):

    @staticmethod
    @abstractmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':  # pragma: no cover
        ...

    @abstractmethod
    def __init__(self, *,
                 logger: 'Logger',
                 **kwargs: Any) -> None:  # pragma: no cover
        ...

    @abstractmethod
    def __call__(self, **kwargs: Any) -> 'Bom':  # pragma: no cover
        ...


from enum import Enum


class PropertyName(Enum):
    # region python
    # TODO: register -- name might not be final, find better one
    PackageExtra = 'cdx:python:package:extra'
    # endregion python

    # region poetry
    # see https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/poetry.md
    PoetryGroup = 'cdx:poetry:group'
    # endregion poetry

    # region pipenv
    # see https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/pipenv.md
    PipenvCategory = 'cdx:pipenv:category'
    # endregion pipenv
