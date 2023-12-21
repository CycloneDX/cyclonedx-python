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

from typing import TYPE_CHECKING, Generator, List

from cyclonedx.model import ExternalReferenceType

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info >= (3, 10):
        from importlib.metadata import PackageMetadata
    else:
        from email.message import Message as PackageMetadata

    from cyclonedx.model import ExternalReference
    from cyclonedx.model.license import License


def metadata2licenses(metadata: 'PackageMetadata') -> Generator['License', None, None]:
    from cyclonedx.factory.license import LicenseFactory

    from .pep621 import classifiers2licenses
    lfac = LicenseFactory()
    if 'Classifier' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#classifier-multiple-use
        classifiers: List[str] = metadata.get_all('Classifier')  # type:ignore[assignment]
        yield from classifiers2licenses(classifiers, lfac)
    if 'License' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#license
        yield lfac.make_from_string(metadata['License'])


def metadata2extrefs(metadata: 'PackageMetadata') -> Generator['ExternalReference', None, None]:
    from cyclonedx.exception.model import InvalidUriException
    from cyclonedx.model import ExternalReference, XsUri

    from .cdx import url_label_to_ert

    if 'Home-page' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#home-page
        try:
            yield ExternalReference(
                type=ExternalReferenceType.WEBSITE,
                url=XsUri(metadata['Home-page'])
            )
        except InvalidUriException:
            pass
    if 'Download-URL' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#download-url
        try:
            yield ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(metadata['Download-URL'])
            )
        except InvalidUriException:
            pass
    for label_url in metadata.get_all('Project-URL', ()):
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use
        label, url = label_url.split(',', maxsplit=1)
        try:
            yield ExternalReference(
                type=url_label_to_ert(label),
                url=XsUri(url.strip()),
                comment=f'Project-URL: {label}',
            )
        except InvalidUriException:
            pass