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
initialize this testbed.
"""

from os import name as os_name
from os.path import dirname, join
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)


if __name__ == '__main__':
    main()
