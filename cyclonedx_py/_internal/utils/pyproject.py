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

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from cyclonedx.factory.license import LicenseFactory

from .cdx import licenses_fixup
from .pep621 import (
    project2component as pep621_project2component,
    project2dependencies as pep621_project2dependencies,
    project2licenses as pep621_project2licenses,
)
from .pep639 import project2licenses as pep639_project2licenses
from .poetry import poetry2component, poetry2dependencies
from .toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.component import Component, ComponentType
    from packaging.requirements import Requirement


def pyproject2component(data: dict[str, Any], *,
                        ctype: 'ComponentType',
                        fpath: str,
                        gather_license_texts: bool,
                        logger: 'Logger'
                        ) -> 'Component':
    tool = data.get('tool', {})
    if poetry := tool.get('poetry'):
        return poetry2component(poetry, ctype=ctype)
    if project := data.get('project'):
        component = pep621_project2component(project, ctype=ctype)
        # region licenses
        lfac = LicenseFactory()
        component.licenses.update(pep639_project2licenses(project, lfac, gather_license_texts,
                                                          fpath=fpath, logger=logger))
        if len(component.licenses) == 0:
            # According to PEP 639 spec, if licenses are declared in the "new" style,
            # all other license declarations MUST be ignored.
            # https://peps.python.org/pep-0639/#converting-legacy-metadata
            component.licenses.update(pep621_project2licenses(project, lfac, gather_license_texts, fpath=fpath))
        licenses_fixup(component)
        # endregion licenses
        return component
    raise ValueError('Unable to build component from pyproject')


def pyproject_load(pyproject_file: str) -> dict[str, Any]:
    try:
        pyproject_fh = open(pyproject_file, encoding='utf8', errors='replace')
    except OSError as err:
        raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
    with pyproject_fh:
        return toml_loads(pyproject_fh.read())


def pyproject_file2component(pyproject_file: str, *,
                             ctype: 'ComponentType',
                             gather_license_texts: bool,
                             logger: 'Logger'
                             ) -> 'Component':
    return pyproject2component(
        pyproject_load(pyproject_file),
        ctype=ctype, fpath=pyproject_file,
        gather_license_texts=gather_license_texts,
        logger=logger
    )


def pyproject2dependencies(data: dict[str, Any]) -> Iterator['Requirement']:
    tool = data.get('tool', {})
    if 'poetry' in tool:
        return poetry2dependencies(tool['poetry'])
    if 'project' in data:
        return pep621_project2dependencies(data['project'])
    return iter(())
