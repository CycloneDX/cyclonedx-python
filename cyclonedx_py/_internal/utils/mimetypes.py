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

_ext_mime_map = {
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    'md': 'text/markdown',
    'txt': 'text/plain',
    'rst': 'text/prs.fallenstein.rst',
    # add more mime types. pull-requests welcome!
}


def guess_type(file_name: str) -> Optional[str]:
    """
    The stdlib `mimetypes.guess_type()` is inconsistent, as it depends heavily on type registry in the env/os.
    Therefore, this polyfill exists.
    """
    ext = splitext(file_name)[1][1:].lower()
    return _ext_mime_map.get(ext) \
        or _stdlib_guess_type(file_name)[0]
