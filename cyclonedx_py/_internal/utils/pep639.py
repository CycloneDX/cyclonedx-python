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
from collections.abc import Generator
from glob import glob
from os.path import dirname, join
from typing import TYPE_CHECKING, Any

from cyclonedx.model import AttachedText, Encoding
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from .bytes import bytes2str
from .mimetypes import guess_type

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import Distribution
    from logging import Logger

    from cyclonedx.factory.license import LicenseFactory
    from cyclonedx.model.license import License


def project2licenses(project: dict[str, Any], lfac: 'LicenseFactory',
                     gather_texts: bool, *,
                     fpath: str) -> Generator['License', None, None]:
    lack = LicenseAcknowledgement.DECLARED
    if isinstance(plicense := project.get('license'), str) \
            and len(plicense) > 0:
        # https://peps.python.org/pep-0639/#add-string-value-to-license-key
        yield lfac.make_from_string(plicense,
                                    license_acknowledgement=lack)
    if gather_texts and isinstance(plfiles := project.get('license-files'), list):
        # https://peps.python.org/pep-0639/#add-license-files-key
        plfiles_root = dirname(fpath)
        for plfile_glob in plfiles:
            for plfile in glob(plfile_glob, root_dir=plfiles_root):
                # per spec:
                # > Tools MUST assume that license file content is valid UTF-8 encoded text
                # anyway, we don't trust this and assume binary
                with open(join(plfiles_root, plfile), 'rb') as plicense_fileh:
                    yield DisjunctiveLicense(name=f'declared license file: {plfile}',
                                             acknowledgement=lack,
                                             text=AttachedText(encoding=Encoding.BASE_64,
                                                               content=b64encode(plicense_fileh.read()).decode()))
    # Silently skip any other types (including string/PEP 621)
    return None


# per spec > license files are stored in the `.dist-info/licenses/` subdirectory of the produced wheel.
# but in practice, other locations are used, too.
_LICENSE_LOCATIONS = ('licenses', 'license_files', '')


def dist2licenses(
    dist: 'Distribution', lfac: 'LicenseFactory',
    gather_texts: bool,
    logger: 'Logger'
) -> Generator['License', None, None]:
    lack = LicenseAcknowledgement.DECLARED
    metadata = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
    if (lexp := metadata['License-Expression']) is not None:
        # see spec: https://peps.python.org/pep-0639/#add-license-expression-field
        yield lfac.make_from_string(lexp,
                                    license_acknowledgement=lack)
    if gather_texts:
        for mlfile in set(metadata.get_all('License-File', ())):
            # see spec: https://peps.python.org/pep-0639/#add-license-file-field
            # latest spec rev: https://discuss.python.org/t/pep-639-round-3-improving-license-clarity-with-better-package-metadata/53020  # noqa: E501
            content = None
            for mlpath in _LICENSE_LOCATIONS:
                try:
                    content = dist.read_text(join(mlpath, mlfile))
                except UnicodeDecodeError as err:
                    try:
                        content = bytes2str(err.object)
                    except UnicodeDecodeError:
                        pass
                    else:
                        break  # for-loop
                else:
                    if content is not None:
                        break  # for-loop
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
