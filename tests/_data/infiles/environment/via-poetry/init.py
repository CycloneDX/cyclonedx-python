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

from os import environ
from os.path import dirname
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable

__all__ = ['main']

this_dir = dirname(__file__)


poetry_env = environ.copy()
poetry_env['VIRTUAL_ENV'] = ''


def poetry_run(*args: str) -> CompletedProcess:
    # Poetry is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'poetry',
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, env=poetry_env, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def main() -> None:
    poetry_run('install', '--no-dev', '--sync',
               '--no-interaction', '--no-ansi')


if __name__ == '__main__':
    main()
