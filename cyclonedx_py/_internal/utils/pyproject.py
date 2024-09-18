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


# use pyproject from pep621
# use pyproject from poetry implementation

from typing import TYPE_CHECKING, Any, Dict, Iterator

from .pep621 import project2component, project2dependencies
from .poetry import poetry2component, poetry2dependencies
from .toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from cyclonedx.model.component import Component, ComponentType
    from packaging.requirements import Requirement


def pyproject2component(data: Dict[str, Any], *,
                        ctype: 'ComponentType', fpath: str) -> 'Component':
    tool = data.get('tool', {})
    if poetry := tool.get('poetry'):
        return poetry2component(poetry, ctype=ctype)
    if project := data.get('project'):
        return project2component(project, ctype=ctype, fpath=fpath)
    raise ValueError('Unable to build component from pyproject')


def pyproject_load(pyproject_file: str) -> Dict[str, Any]:
    try:
        pyproject_fh = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
    except OSError as err:
        raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
    with pyproject_fh:
        return toml_loads(pyproject_fh.read())


def pyproject_file2component(pyproject_file: str, *,
                             ctype: 'ComponentType') -> 'Component':
    return pyproject2component(
        pyproject_load(pyproject_file),
        ctype=ctype, fpath=pyproject_file
    )


def pyproject2dependencies(data: Dict[str, Any]) -> Iterator['Requirement']:
    tool = data.get('tool', {})
    if 'poetry' in tool:
        return poetry2dependencies(tool['poetry'])
    if 'project' in data:
        return project2dependencies(data['project'])
    return iter(())
