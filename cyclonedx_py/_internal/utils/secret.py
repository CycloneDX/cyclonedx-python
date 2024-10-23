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

from re import compile as re_compile

_URL_AUTH_MATCHER = re_compile(r'(?<=://)[^/@:]+:[^/@]+@')
_URL_AUTH_REPLACE = ''  # drop auth - in accordance with PEP 610


def redact_auth_from_url(s: str) -> str:
    # is intended to work on any string that contains an url.
    return _URL_AUTH_MATCHER.sub(_URL_AUTH_REPLACE, s) \
        if '@' in s \
        else s
