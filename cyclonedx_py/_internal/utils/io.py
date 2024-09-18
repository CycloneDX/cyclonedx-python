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

from sys import getdefaultencoding
from tempfile import NamedTemporaryFile
from typing import BinaryIO

from chardet import detect as chardetect


def io2str(io: BinaryIO, *, errors: str = 'strict') -> str:
    data = io.read()
    # see https://docs.python.org/3/library/codecs.html#standard-encodings
    encoding = (chardetect(data)['encoding'] or getdefaultencoding()).replace(
        # replace Windows-encoding with code-page
        'Windows-', 'cp')
    return data.decode(encoding, errors)


def io2file(io: BinaryIO, *, errors: str = 'strict') -> str:
    # prevent issues on windows: https://github.com/python/cpython/issues/58451
    tf = NamedTemporaryFile('wt', delete=False,
                            # we prefer utf8 encoded strings, but ...
                            # - must not change newlines
                            # - must not change encoding, fallback to system encoding for compatibility
                            newline='', encoding=None)
    tf.write(io2str(io, errors=errors))
    tf.close()
    return tf.name
