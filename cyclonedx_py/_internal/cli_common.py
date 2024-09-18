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


from typing import TYPE_CHECKING

from cyclonedx.model.component import ComponentType

from .utils.args import argparse_type4enum

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Action, ArgumentParser


def add_argument_pyproject(p: 'ArgumentParser') -> 'Action':
    return p.add_argument('--pyproject',
                          metavar='<file>',
                          help="Path to the root component's `pyproject.toml` file. "
                               'This should point to a file compliant with PEP 621 '
                               '(storing project metadata).',
                          dest='pyproject_file',
                          default=None)


def add_argument_mc_type(p: 'ArgumentParser') -> 'Action':
    choices = [ComponentType.APPLICATION,
               ComponentType.FIRMWARE,
               ComponentType.LIBRARY]
    return p.add_argument('--mc-type',
                          metavar='<type>',
                          help='Type of the main component'
                               f' {{choices: {", ".join(t.value for t in choices)}}}'
                               ' (default: %(default)s)',
                          dest='mc_type',
                          choices=choices,
                          type=argparse_type4enum(ComponentType),
                          default=ComponentType.APPLICATION.value)
