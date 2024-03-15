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

# !! version is managed by `semantic_release`
# do not use typing here, or else `semantic_release` might have issues finding the variable
__version__ = "4.1.3"  # noqa:Q000

# There is no stable/public API.
# However, you might call the stable CLI instead, like so:
#   from sys import executable
#   from subprocess import run
#   run((executable, '-m', 'cyclonedx_py', '--help'))
