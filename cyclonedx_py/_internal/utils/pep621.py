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


"""
Functionality related to PEP 621

See https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#declaring-project-metadata
See https://peps.python.org/pep-0621/
"""

from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable

if TYPE_CHECKING:
    from cyclonedx.factory.license import LicenseFactory
    from cyclonedx.model.component import Component, ComponentType
    from cyclonedx.model.license import License


def classifiers2licenses(classifiers: Iterable[str], lfac: 'LicenseFactory') -> Generator['License', None, None]:
    from .license_trove_classifier import license_trove2spdx
    yield from map(lfac.make_from_string,
                   # `lfac.make_with_id` could be a shortcut,
                   # but some SPDX ID might not (yet) be known to CDX.
                   # So better go with `lfac.make_from_string` and be safe.
                   filter(None,
                          map(license_trove2spdx,
                              classifiers)))


def pyproject2licenses(pyproject: Dict[str, Any], lfac: 'LicenseFactory') -> Generator['License', None, None]:
    if 'classifiers' in pyproject:
        # https://packaging.python.org/en/latest/specifications/pyproject-toml/#classifiers
        # https://peps.python.org/pep-0621/#classifiers
        # https://packaging.python.org/en/latest/specifications/core-metadata/#classifier-multiple-use
        yield from classifiers2licenses(pyproject['classifiers'], lfac)
    license = pyproject.get('license')
    # https://packaging.python.org/en/latest/specifications/pyproject-toml/#license
    # https://peps.python.org/pep-0621/#license
    # https://packaging.python.org/en/latest/specifications/core-metadata/#license
    if isinstance(license, dict) and 'text' in license:
        yield lfac.make_from_string(license['text'])


def pyproject2component(pyproject: Dict[str, Any], *,
                        type: 'ComponentType') -> 'Component':
    from cyclonedx.factory.license import LicenseFactory
    from cyclonedx.model.component import Component

    from .cdx import licenses_fixup

    project = pyproject['project']
    return Component(
        type=type,
        name=project['name'],
        version=project.get('version', None),
        description=project.get('description', None),
        licenses=licenses_fixup(pyproject2licenses(project, LicenseFactory())),
        # TODO add more properties according to spec
        # extRefs with .cdx.url_label_to_ert()
    )


def pyproject_load(pyproject_file: str) -> Dict[str, Any]:
    from .toml import toml_loads
    try:
        pyproject_fh = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
    except OSError as err:
        raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
    with pyproject_fh:
        return toml_loads(pyproject_fh.read())


def pyproject_file2component(pyproject_file: str, *,
                             type: 'ComponentType') -> 'Component':
    return pyproject2component(
        pyproject_load(pyproject_file),
        type=type
    )


def pyproject_dependencies(pyproject: Dict[str, Any]) -> Generator[str, None, None]:
    yield from pyproject.get('dependencies', ())
    for opts in pyproject.get('optional-dependencies', {}).values():
        yield from opts
