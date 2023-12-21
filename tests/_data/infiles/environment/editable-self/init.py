# This file is part of CycloneDX Python Lib
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
initialize this test bed.
"""

from os import name as os_name
from os.path import dirname, join
from subprocess import check_call  # nosec:B404
from sys import executable
from venv import EnvBuilder

__all__ = ['main']

env_dir = join(dirname(__file__), '.venv')


def pip_install(*args: str) -> None:
    # pip is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pip',
        '--python', env_dir,
        'install', '--require-virtualenv', '--no-input', '--progress-bar=off', '--no-color',
        *args
    )
    print('+ ', *call)
    check_call(call, shell=False)  # nosec:B603


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)
    pip_install('-e', dirname(__file__))


if __name__ == '__main__':
    main()