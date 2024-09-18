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
from os.path import abspath, dirname, join
from subprocess import check_call  # nosec:B404
from sys import executable
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')

localpackages_dir = abspath(join(dirname(__file__), '..', '..', '_helpers', 'local_pckages'))


def pip_install(*args: str) -> None:
    # pip is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pip',
        '--python', env_dir,
        'install', '--require-virtualenv', '--no-input', '--progress-bar=off', '--no-color',
        *args
    )
    print('+ ', *call)
    check_call(call, cwd=this_dir, shell=False)  # nosec:B603


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)

    pip_install(
        join(localpackages_dir, 'a', 'dist', 'package_a-23.42-py3-none-any.whl'),
        join(localpackages_dir, 'b', 'dist', 'package-b-23.42.tar.gz'),
        join(localpackages_dir, 'c'),
    )


if __name__ == '__main__':
    main()
