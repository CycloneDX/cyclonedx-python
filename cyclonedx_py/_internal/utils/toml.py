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


__all__ = ['toml_loads']

import sys

# TOML polyfill: https://github.com/hukkin/tomli#intro
# > A version of `tomli`, the `tomllib` module, was added to the standard library in Python 3.11 via PEP 680.
# > `Tomli` continues to provide a backport on PyPI for Python versions
# > where the standard library module is not available and that have not yet reached their end-of-life.
if sys.version_info >= (3, 11):
    from tomllib import loads as toml_loads
else:
    from tomli import loads as toml_loads
