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
from typing import TYPE_CHECKING, Generator, Set, Union

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import AttachedText, Encoding
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from .io import io2str
from .mimetypes import guess_type

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import Distribution
    from logging import Logger

    from cyclonedx.model.license import License


def _try_load(dist: 'Distribution', metadir: str, filename: str) -> Union[str, None]:
    # Might raise NotImplementedError in theory
    # but nothing we can do in that case.
    try:
        candidate = dist.locate_file(join(metadir, filename))
    except NotImplementedError:
        return None

    if not candidate:
        return None

    try:
        with open(str(candidate), 'rb') as fin:
            return io2str(fin)
    except FileNotFoundError:
        pass
    return None


def handle_bad_license_file_encoding(
    dist: 'Distribution',
    lfile: str,
    logger: 'Logger'
) -> Union[str, None]:
    # Distribution has no method to find the actual metadata dir,
    # e.g. dist-info or egg-info.
    # So we mimic the logic in PathDistribution and check both subdirs
    content: Union[str, None] = None
    for metadir in ('.dist-info', '.egg-info'):
        content = _try_load(dist, metadir, lfile)
        if content:
            break

    if content is None:
        logger.debug('Error: license file %r for dist %r is not UTF-8 encoded',
                     lfile, dist.metadata['Name'])
    return content


def gather_license_texts(
    dist: 'Distribution',
    lfiles: Set[str],
    logger: 'Logger'
) -> Generator['License', None, None]:
    lack = LicenseAcknowledgement.DECLARED
    for mlfile in lfiles:
        # see spec: https://peps.python.org/pep-0639/#add-license-file-field
        # latest spec rev: https://discuss.python.org/t/pep-639-round-3-improving-license-clarity-with-better-package-metadata/53020  # noqa: E501

        # per spec > license files are stored in the `.dist-info/licenses/` subdirectory of the produced wheel.
        # but in practice, other locations are used, too.
        # loop over the candidate location and pick the first one found.
        malformed = None
        content = None
        for loc in ('licenses', 'license_files', '.'):
            path = join(loc, mlfile)
            try:
                content = dist.read_text(path)
            except UnicodeDecodeError:
                # Malformed, stop looking
                malformed = path
                break

            if content is not None:
                break

        if content is None and malformed:
            # Try a little harder
            content = handle_bad_license_file_encoding(dist, malformed, logger)

        if content is None:
            logger.debug('Error: failed to read license file %r for dist %r',
                         mlfile, dist.metadata['Name'])
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


def dist2licenses(
    dist: 'Distribution',
    gather_text: bool,
    logger: 'Logger'
) -> Generator['License', None, None]:
    metadata = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
    if (lexp := metadata['License-Expression']) is not None:
        lfac = LicenseFactory()
        lack = LicenseAcknowledgement.DECLARED
        # see spec: https://peps.python.org/pep-0639/#add-license-expression-field
        yield lfac.make_from_string(lexp,
                                    license_acknowledgement=lack)
    if gather_text and (lfiles := set(fn for fn in metadata.get_all('License-File', ()))):
        yield from gather_license_texts(dist, lfiles, logger)
