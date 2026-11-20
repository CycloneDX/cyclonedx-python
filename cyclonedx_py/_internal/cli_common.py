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


from typing import TYPE_CHECKING, Optional

from cyclonedx.model.component import Component, ComponentType

from .utils.args import argparse_type4enum
from .utils.pyproject import pyproject_file2component

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Action, ArgumentParser
    from logging import Logger


def add_argument_pyproject(p: 'ArgumentParser') -> 'Action':
    return p.add_argument('--pyproject',
                          metavar='<file>',
                          help="Path to the root component's `pyproject.toml` file.\n"
                               'This should point to a file compliant with PEP 621 '
                               '(Storing project metadata in pyproject.toml). '
                               'Supports PEP 639 (Improving License Clarity with Better Package Metadata). ',
                          dest='pyproject_file',
                          default=None)


def add_argument_mc_name(p: 'ArgumentParser') -> 'Action':
    return p.add_argument('--mc-name',
                          metavar='<name>',
                          help='Name of the main component. '
                               'Overrides `pyproject.toml` metadata when provided.',
                          dest='mc_name',
                          default=None)


def add_argument_mc_version(p: 'ArgumentParser') -> 'Action':
    return p.add_argument('--mc-version',
                          metavar='<version>',
                          help='Version of the main component. '
                               'Overrides `pyproject.toml` metadata when provided.',
                          dest='mc_version',
                          default=None)


def add_argument_mc_type(p: 'ArgumentParser') -> 'Action':
    choices = [ComponentType.APPLICATION,
               ComponentType.FIRMWARE,
               ComponentType.LIBRARY]
    return p.add_argument('--mc-type',
                          metavar='<type>',
                          help='Type of the main component.'
                               f' {{choices: {", ".join(t.value for t in choices)}}}'
                               ' (default: %(default)s)',
                          dest='mc_type',
                          choices=choices,
                          type=argparse_type4enum(ComponentType),
                          default=ComponentType.APPLICATION.value)


def resolve_main_component(*,  # noqa: PLR0913
                           mc_name: Optional[str],
                           mc_version: Optional[str],
                           mc_type: 'ComponentType',
                           pyproject_file: Optional[str] = None,
                           gather_license_texts: bool,
                           logger: 'Logger') -> Optional[Component]:
    """Resolve main component metadata from CLI args and/or pyproject.toml.

    Precedence:
    1. If pyproject_file is provided, load and use it as base
    2. CLI args (mc_name, mc_version) override pyproject values if provided
    3. If neither pyproject nor mc_name is provided, return None
    """
    component: Optional[Component] = None

    if pyproject_file is not None:
        component = pyproject_file2component(pyproject_file, ctype=mc_type,
                                             gather_license_texts=gather_license_texts, logger=logger)
    elif mc_name is None:
        return None
    else:
        # Create minimal component from CLI args only
        component = Component(type=mc_type, name=mc_name, version=mc_version)

    # Apply CLI overrides
    if mc_name is not None:
        component.name = mc_name
    if mc_version is not None:
        component.version = mc_version
    component.type = mc_type
    component.bom_ref.value = 'root-component'
    return component

