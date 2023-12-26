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


from argparse import ArgumentTypeError
from enum import Enum
from typing import Callable, List, Type, TypeVar

_E = TypeVar('_E', bound=Enum)


def argparse_type4enum(enum: Type[_E]) -> Callable[[str], _E]:
    def str2case(value: str) -> _E:
        try:
            return enum[value.upper()]
        except KeyError:
            raise ArgumentTypeError(f'unsupported value {value!r}')

    return str2case


def choices4enum(enum: Type[Enum]) -> str:
    return f'{{choices: {", ".join(sorted(c.name for c in enum))}}}'


def arparse_split(*seps: str) -> Callable[[str], List[str]]:
    def str_split(value: str) -> List[str]:
        sep = seps[0]
        for s in seps[1:]:
            value = value.replace(s, sep)
        return list(filter(None, map(str.strip, value.split(sep))))

    return str_split
