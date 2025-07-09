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
from os.path import dirname, join
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, Union

from cyclonedx.model import AttachedText, Encoding
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from ..py_interop.glob import glob
from .mimetypes import guess_type

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import Distribution
    from logging import Logger

    from cyclonedx.factory.license import LicenseFactory
    from cyclonedx.model.license import License


def project2licenses(project: dict[str, Any], lfac: 'LicenseFactory',
                     gather_texts: bool, *,
                     fpath: str,
                     logger: 'Logger') -> Generator['License', None, None]:
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
            for plfile in glob(join(*PurePosixPath(plfile_glob).parts), root_dir=plfiles_root, recursive=True):
                # per spec:
                # > Tools MUST assume that license file content is valid UTF-8 encoded text
                # anyway, we don't trust this and assume binary
                try:
                    plicense_fileh = open(join(plfiles_root, plfile), 'rb')
                except Exception as err:  # pragma: nocover
                    logger.debug('Error: failed to read license file %r for project %r: %r',
                                 plfile, project.get('name', '<unnamed>'), err)
                    del err
                    continue
                with plicense_fileh:
                    content = plicense_fileh.read()
                yield _make_license_from_content(plfile, content, lack)
    # Silently skip any other types (including string/PEP 621)
    return None


# Per PEP 639 spec, license files are stored in the `.dist-info/` directory of the produced wheel.
# see https://peps.python.org/pep-0639/#add-license-file-field
# Put in reality, other locations are used, too...
_LICENSE_LOCATIONS = ('', 'licenses', 'license_files')


def dist2licenses_from_files(
    dist: 'Distribution',
    logger: 'Logger'
) -> Generator['License', None, None]:
    lack = LicenseAcknowledgement.DECLARED
    metadata = dist.metadata  # see https://packaging.python.org/en/latest/specifications/core-metadata/
    for mlfile in set(metadata.get_all('License-File', ())):
        # see spec: https://peps.python.org/pep-0639/#add-license-file-field
        # latest spec rev: https://discuss.python.org/t/pep-639-round-3-improving-license-clarity-with-better-package-metadata/53020  # noqa: E501
        content: Union[None, str, bytes] = None
        for mlpath in _LICENSE_LOCATIONS:
            try:
                content = dist.read_text(join(mlpath, mlfile))
                break  # for-loop
            except UnicodeDecodeError as err:
                content = err.object
                break  # for-loop
            except Exception:
                pass  # nosec B110
        if content is None:  # pragma: no cover
            logger.debug('Error: failed to read license file %r for dist %r',
                         mlfile, metadata['Name'])
            continue  # for-loop
        yield _make_license_from_content(mlfile, content, lack)


def _make_license_from_content(file_name: str, content: Union[str, bytes],
                               lack: 'LicenseAcknowledgement') -> DisjunctiveLicense:
    # In the past, we did best-effort decoding to string,
    # see https://github.com/CycloneDX/cyclonedx-python/blob/b7a8f64ae212c5a5fd6b7cf8c83851ba692df256/cyclonedx_py/_internal/utils/pep639.py#L67-L71  # noqa:E501
    # But this was dropped, in favour of base64 encoding; CycloneDX is for machines, not humans!
    content_type = guess_type(file_name) or AttachedText.DEFAULT_CONTENT_TYPE
    return DisjunctiveLicense(
        name=f'{lack.value} license file: {"/".join(Path(file_name).parts)}',
        acknowledgement=lack,
        text=AttachedText(
            content_type=content_type,
            encoding=Encoding.BASE_64,
            # Per PEP 639 spec, license files are human-readable texts.
            # But in reality, we found non-printable bytes in some files!
            content=b64encode(
                content
                if isinstance(content, bytes)
                else content.encode('utf-8')
            ).decode('ascii')))
