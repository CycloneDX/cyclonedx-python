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

from unittest import TestCase

from ddt import data, ddt, unpack

from cyclonedx_py._internal.utils.secret import redact_auth_from_url


@ddt
class TestRedactAuthFromUrl(TestCase):

    @data(
        # user and password
        ('https://user:pass@example.com/simple', 'https://example.com/simple'),
        ('https://user:p@ss@example.com/simple', 'https://example.com/simple'),
        ('ssh://git:pass@example.com/foo.git', 'ssh://example.com/foo.git'),
        # single token
        ('https://0123456789abcdef@example.com/simple', 'https://example.com/simple'),
        ('HTTP://0123456789abcdef@example.com:8080/simple', 'HTTP://example.com:8080/simple'),
        ('https://0123456789abcdef:@example.com/simple', 'https://example.com/simple'),
        ('https://:0123456789abcdef@example.com/simple', 'https://example.com/simple'),
        ('git+https://0123456789abcdef@example.com/foo.git@1.2.3', 'git+https://example.com/foo.git@1.2.3'),
        ('foo @ git+https://0123456789abcdef@example.com/foo.git@1.2.3',
         'foo @ git+https://example.com/foo.git@1.2.3'),
        ('https://0123456789abcdef@example.com?a=b@c', 'https://example.com?a=b@c'),
    )
    @unpack
    def test_redacts(self, url: str, expected: str) -> None:
        self.assertEqual(expected, redact_auth_from_url(url))

    @data(
        'https://example.com/simple',
        'https://example.com:8080/foo@1.2.3',
        'https://example.com?user@example.com',
        'https://example.com#user@example.com',
        'git+https://example.com/foo.git@1.2.3',
        'git+ssh://git@example.com/foo.git',
        'git@example.com:foo.git',
        'foo @ https://example.com/foo.tar.gz',
        'https://example.com user@example.com',
    )
    def test_keeps(self, url: str) -> None:
        self.assertEqual(url, redact_auth_from_url(url))
