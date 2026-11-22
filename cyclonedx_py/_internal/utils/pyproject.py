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
from .poetry import poetry2component, poetry2dependencies, poetry2extrefs, poetry2licenses
from .toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.component import Component, ComponentType
    from packaging.requirements import Requirement


def _merge_poetry_into_component(component: 'Component',
                                 project: dict[str, Any],
                                 poetry: dict[str, Any],
                                 lfac: 'LicenseFactory',
                                 has_pep639_licenses: bool) -> None:
    if component.version is None:
        component.version = poetry.get('version')
    if component.description is None:
        component.description = poetry.get('description')

    existing_extrefs = {(er.type, er.url) for er in component.external_references}
    for er in poetry2extrefs(poetry):
        if (er.type, er.url) not in existing_extrefs:
            component.external_references.add(er)
            existing_extrefs.add((er.type, er.url))

    if not has_pep639_licenses:
        fallback_keys = ('license', 'classifiers')
        poetry_fallback = {k: poetry[k] for k in fallback_keys if k not in project and k in poetry}
        component.licenses.update(poetry2licenses(poetry_fallback, lfac))


def pyproject2component(data: dict[str, Any], *,
                        ctype: 'ComponentType',
                        fpath: str,
                        gather_license_texts: bool,
                        logger: 'Logger'
                        ) -> 'Component':
    project: dict[str, Any] = data.get('project', {})
    poetry: dict[str, Any] = data.get('tool', {}).get('poetry', {})
    if project:
        if 'name' not in project and 'name' in poetry:
            project = {**project, 'name': poetry['name']}
        component = pep621_project2component(project, ctype=ctype)
        # region licenses
        lfac = LicenseFactory()
        component.licenses.update(pep639_project2licenses(project, lfac, gather_license_texts,
                                                          fpath=fpath, logger=logger))
        has_pep639_licenses = len(component.licenses) > 0
        if not has_pep639_licenses:
            # According to PEP 639 spec, if licenses are declared in the "new" style,
            # all other license declarations MUST be ignored.
            # https://peps.python.org/pep-0639/#converting-legacy-metadata
            component.licenses.update(pep621_project2licenses(project, lfac, gather_license_texts, fpath=fpath))
        if poetry:
            _merge_poetry_into_component(component, project, poetry, lfac, has_pep639_licenses)
        licenses_fixup(component)
        # endregion licenses
        return component
    if poetry:
        return poetry2component(poetry, ctype=ctype)
    raise ValueError('Unable to build component from pyproject: pyproject.toml is not PEP 621-compliant')


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
    if project := data.get('project'):
        yield from pep621_project2dependencies(project)
    if poetry := data.get('tool', {}).get('poetry'):
        yield from poetry2dependencies(poetry)
