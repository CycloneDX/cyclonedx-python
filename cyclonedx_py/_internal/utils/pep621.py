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


"""functionality related tot PEP 621
See https://peps.python.org/pep-0621/
See https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#declaring-project-metadata
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from cyclonedx.model.component import Component, ComponentType


def pyproject2component(pyproject: Dict[str, Any], *,
                        type: 'ComponentType') -> 'Component':
    from cyclonedx.model.component import Component

    project = pyproject['project']
    return Component(
        type=type,
        name=project['name'],
        version=project.get('version', None),
        description=project.get('description', None),
        # TODO add more properties according to spec
    )


def pyproject_file2component(pyproject_file: str, *,
                             type: 'ComponentType') -> 'Component':
    from .toml import toml_loads

    try:
        pyproject_fh = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
    except OSError as err:
        raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
    with pyproject_fh:
        return pyproject2component(
            toml_loads(pyproject_fh.read()),
            type=type
        )