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

from cyclonedx.exception.model import InvalidUriException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri

from .cdx import url_label_to_ert
from .pep621 import classifiers2licenses

if TYPE_CHECKING:  # pragma: no cover
    import sys

    from cyclonedx.model.license import License

    if sys.version_info >= (3, 10):
        from importlib.metadata import PackageMetadata
    else:
        from email.message import Message as PackageMetadata


def metadata2licenses(metadata: 'PackageMetadata') -> Generator['License', None, None]:
    lfac = LicenseFactory()
    if 'Classifier' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#classifier-multiple-use
        classifiers: List[str] = metadata.get_all('Classifier')  # type:ignore[assignment]
        yield from classifiers2licenses(classifiers, lfac)
    if 'License' in metadata:
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#license
        yield lfac.make_from_string(metadata['License'])


def metadata2extrefs(metadata: 'PackageMetadata') -> Generator['ExternalReference', None, None]:
    for meta_key, extref_typet in (
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#home-page
        ('Home-page', ExternalReferenceType.WEBSITE),
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#download-url
        ('Download-URL', ExternalReferenceType.DISTRIBUTION),
    ):
        if meta_key in metadata:
            try:
                yield ExternalReference(
                    comment=f'from packaging metadata: {meta_key}',
                    type=extref_typet,
                    url=XsUri(metadata[meta_key]))
            except InvalidUriException:  # pragma: nocover
                pass
    for label_url in metadata.get_all('Project-URL', ()):
        # see https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use
        label, url = label_url.split(',', maxsplit=1)
        try:
            yield ExternalReference(
                comment=f'from packaging metadata Project-URL: {label}',
                type=url_label_to_ert(label),
                url=XsUri(url.strip()))
        except InvalidUriException:  # pragma: nocover
            pass
