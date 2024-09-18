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

"""
Functionality related to poetry manifest.

See https://python-poetry.org/docs/pyproject/
"""

from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, Generator, List

from cyclonedx.exception.model import InvalidUriException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri
from cyclonedx.model.component import Component
from cyclonedx.model.license import LicenseAcknowledgement
from packaging.requirements import Requirement

from .cdx import licenses_fixup, url_label_to_ert
from .pep621 import classifiers2licenses

if TYPE_CHECKING:
    from cyclonedx.model.component import ComponentType
    from cyclonedx.model.license import License


def poetry2extrefs(poetry: Dict[str, Any]) -> Generator['ExternalReference', None, None]:
    for ers, ert in (
        ('homepage', ExternalReferenceType.WEBSITE),
        ('repository', ExternalReferenceType.VCS),
        ('documentation', ExternalReferenceType.DOCUMENTATION),
    ):
        try:
            yield ExternalReference(
                comment=f'from poetry: {ers}',
                type=ert,
                url=XsUri(str(poetry[ers])))
        except (KeyError, InvalidUriException):  # pragma: nocover
            pass
    for label, url in poetry.get('urls', {}).items():
        try:
            yield ExternalReference(
                comment=f'from poetry url: {label}',
                type=url_label_to_ert(label),
                url=XsUri(str(url)))
        except InvalidUriException:  # pragma: nocover
            pass


def poetry2component(poetry: Dict[str, Any], *, ctype: 'ComponentType') -> 'Component':
    licenses: List['License'] = []
    lfac = LicenseFactory()
    lack = LicenseAcknowledgement.DECLARED
    if 'classifiers' in poetry:
        licenses.extend(classifiers2licenses(poetry['classifiers'], lfac, lack))
    if 'license' in poetry:
        # per spec(https://python-poetry.org/docs/pyproject#license):
        # the `license` is intended to be the name of a license, not the license text itself.
        licenses.append(lfac.make_from_string(poetry['license'],
                                              license_acknowledgement=lack))

    return Component(
        type=ctype,
        name=poetry['name'],
        version=poetry.get('version'),
        description=poetry.get('description'),
        licenses=licenses_fixup(licenses),
        external_references=poetry2extrefs(poetry),
        # TODO add more properties according to spec
    )


def poetry2dependencies(poetry: Dict[str, Any]) -> Generator['Requirement', None, None]:

    for name, spec in chain(
        poetry.get('dependencies', {}).items(),
        poetry.get('dev-dependencies', {}).items(),
        chain.from_iterable(
            group.get('dependencies', {}).items()
            for group in poetry.get('group', {}).values()
        )
    ):
        req = Requirement(name)
        if isinstance(spec, dict) and 'extras' in spec:
            req.extras = set(spec['extras'])
        # add other optional properties as soon as they were needed
        yield req
