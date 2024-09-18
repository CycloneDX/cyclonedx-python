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

__all__ = [  # type:ignore[var-annotated]
    # There is no stable/public API.
    # However, you might call the stable CLI instead, like so:
    #   from sys import executable
    #   from subprocess import run
    #   run((executable, '-m', 'cyclonedx_py', '--help'))
]

from sys import exit

from ._internal.cli import run as _run

exit(_run(prog=f'python -m {__package__}' if __package__ else None))
