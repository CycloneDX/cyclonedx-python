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
Functionality related to PEP 621.

See https://packaging.python.org/en/latest/specifications/declaring-project-metadata/
See https://peps.python.org/pep-0621/
"""

from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable, Iterator

from cyclonedx.exception.model import InvalidUriException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import ExternalReference, XsUri
from cyclonedx.model.component import Component
from packaging.requirements import Requirement

from .cdx import licenses_fixup, url_label_to_ert
from .license_trove_classifier import license_trove2spdx

if TYPE_CHECKING:
    from cyclonedx.model.component import ComponentType
    from cyclonedx.model.license import License


def classifiers2licenses(classifiers: Iterable[str], lfac: 'LicenseFactory') -> Generator['License', None, None]:
    yield from map(lfac.make_from_string,
                   # `lfac.make_with_id` could be a shortcut,
                   # but some SPDX ID might not (yet) be known to CDX.
                   # So better go with `lfac.make_from_string` and be safe.
                   filter(None,
                          map(license_trove2spdx,
                              classifiers)))


def project2licenses(project: Dict[str, Any], lfac: 'LicenseFactory') -> Generator['License', None, None]:
    if 'classifiers' in project:
        # https://packaging.python.org/en/latest/specifications/pyproject-toml/#classifiers
        # https://peps.python.org/pep-0621/#classifiers
        # https://packaging.python.org/en/latest/specifications/core-metadata/#classifier-multiple-use
        yield from classifiers2licenses(project['classifiers'], lfac)
    license = project.get('license')
    # https://packaging.python.org/en/latest/specifications/pyproject-toml/#license
    # https://peps.python.org/pep-0621/#license
    # https://packaging.python.org/en/latest/specifications/core-metadata/#license
    if isinstance(license, dict) and 'text' in license:
        yield lfac.make_from_string(license['text'])


def project2extrefs(project: Dict[str, Any]) -> Generator['ExternalReference', None, None]:
    # see https://packaging.python.org/en/latest/specifications/pyproject-toml/#urls
    for label, url in project.get('urls', {}).items():
        try:
            yield ExternalReference(
                comment=f'from pyproject urls: {label}',
                type=url_label_to_ert(label),
                url=XsUri(str(url)))
        except InvalidUriException:  # pragma: nocover
            pass


def project2component(project: Dict[str, Any], *,
                      type: 'ComponentType') -> 'Component':
    dynamic = project.get('dynamic', ())
    return Component(
        type=type,
        name=project['name'],
        version=project.get('version', None) if 'version' not in dynamic else None,
        description=project.get('description', None) if 'description' not in dynamic else None,
        licenses=licenses_fixup(project2licenses(project, LicenseFactory())),
        external_references=project2extrefs(project),
        # TODO add more properties according to spec
    )


def project2dependencies(project: Dict[str, Any]) -> Iterator['Requirement']:
    return (
        Requirement(dep)
        for dep in chain(
            project.get('dependencies', ()),
            chain.from_iterable(project.get('optional-dependencies', {}).values())
        )
    )
