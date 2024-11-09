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
from subprocess import PIPE, CompletedProcess, run  # nosec:B404
from sys import argv, executable
from typing import Any
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')
constraint_file = join(this_dir, 'pinning.txt')


def pip_run(*args: str, **kwargs: Any) -> CompletedProcess:
    # pip is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pip',
        '--python', env_dir,
        *args
    )
    print('+ ', *call)
    res = run(call, **kwargs, cwd=this_dir, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def pip_install(*args: str) -> None:
    pip_run(
        'install', '--require-virtualenv', '--no-input', '--progress-bar=off', '--no-color',
        '-c', constraint_file,  # needed for reproducibility
        *args
    )


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)

    pip_install(
        '--no-dependencies',
        # with License-Expression
        'attrs',
        # with License-File
        'boolean.py',
        'jsonpointer',
        'license_expression',
        'lxml',
        # with expression-like License AND License-File
        'cryptography==43.0.1',  # https://github.com/CycloneDX/cyclonedx-python/issues/826
    )


if __name__ == '__main__':
    main()
    if '--pin' in argv:
        res = pip_run('freeze', '--all', '--local', stdout=PIPE)
        with open(constraint_file, 'wb') as cf:
            cf.write(res.stdout)
