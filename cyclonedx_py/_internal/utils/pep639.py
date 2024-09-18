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
Functionality related to PEP 639.

See https://peps.python.org/pep-0639/
"""

from base64 import b64encode
from os.path import join
from typing import TYPE_CHECKING, Generator

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import AttachedText, Encoding
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from .mimetypes import guess_type

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import Distribution
    from logging import Logger

    from cyclonedx.model.license import License


def dist2licenses(
    dist: 'Distribution',
    gather_text: bool,
    logger: 'Logger'
) -> Generator['License', None, None]:
    lfac = LicenseFactory()
    lack = LicenseAcknowledgement.DECLARED
    metadata = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
    if (lexp := metadata['License-Expression']) is not None:
        # see spec: https://peps.python.org/pep-0639/#add-license-expression-field
        yield lfac.make_from_string(lexp,
                                    license_acknowledgement=lack)
    if gather_text:
        for mlfile in set(metadata.get_all('License-File', ())):
            # see spec: https://peps.python.org/pep-0639/#add-license-file-field
            # latest spec rev: https://discuss.python.org/t/pep-639-round-3-improving-license-clarity-with-better-package-metadata/53020  # noqa: E501

            # per spec > license files are stored in the `.dist-info/licenses/` subdirectory of the produced wheel.
            # but in practice, other locations are used, too.
            content = dist.read_text(join('licenses', mlfile)) \
                or dist.read_text(join('license_files', mlfile)) \
                or dist.read_text(mlfile)
            if content is None:  # pragma: no cover
                logger.debug('Error: failed to read license file %r for dist %r',
                             mlfile, metadata['Name'])
                continue
            encoding = None
            content_type = guess_type(mlfile) or AttachedText.DEFAULT_CONTENT_TYPE
            # per default, license files are human-readable texts.
            if not content_type.startswith('text/'):
                encoding = Encoding.BASE_64
                content = b64encode(content.encode('utf-8')).decode('ascii')
            yield DisjunctiveLicense(
                name=f'declared license file: {mlfile}',
                acknowledgement=lack,
                text=AttachedText(
                    content=content,
                    encoding=encoding,
                    content_type=content_type
                ))
