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

from mimetypes import guess_type as _stdlib_guess_type
from os.path import splitext
from typing import Optional

_MIME_TEXT_PLAIN = 'text/plain'

_MAP_EXT_MIME = {
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    '.csv': 'text/csv',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '.rst': 'text/prs.fallenstein.rst',
    '.rtf': 'application/rtf',  # our scope is text, yes, but RTF is binary - so we should base64 encode it ...
    '.xml': 'text/xml',  # not `application/xml` -- our scope is text!
    # add more mime types above this line. pull-requests welcome!
    # license-specific files
    '.license': _MIME_TEXT_PLAIN,
    '.licence': _MIME_TEXT_PLAIN,
}

_LICENSE_FNAME_BASE = ('licence', 'license')
_LICENSE_FNAME_EXT = (
    '.apache',
    '.bsd',
    '.gpl',
    '.mit',
)


def guess_type(file_name: str) -> Optional[str]:
    """
    The stdlib `mimetypes.guess_type()` is inconsistent, as it depends heavily on type registry in the env/os.
    Therefore, this polyfill exists.
    """
    file_name_l = file_name.lower()
    base, ext = splitext(file_name_l)
    if ext == '':
        return None
    if base in _LICENSE_FNAME_BASE and ext in _LICENSE_FNAME_EXT:
        return _MIME_TEXT_PLAIN
    return _MAP_EXT_MIME.get(ext) \
        or _stdlib_guess_type(file_name_l)[0]
