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
from os.path import dirname, join
from shutil import rmtree
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable
from typing import Any

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')

pipenv_env = environ.copy()
pipenv_env['PIPENV_VENV_IN_PROJECT'] = '1'
pipenv_env['PIPENV_IGNORE_VIRTUALENVS'] = '1'
pipenv_env['PIPENV_NO_INHERIT'] = '1'
pipenv_env['PIPENV_NOSPIN'] = '1'


def pipenv_run(*args: str) -> CompletedProcess:
    # pipenv is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pipenv',
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, env=pipenv_env, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


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


def main() -> None:
    # needed to reinit partially stripped evn
    rmtree(env_dir, ignore_errors=True)

    # the actual setuo
    pipenv_run('install', '--deploy', '--no-site-packages')

    # uninstall things that were coming with virtualenv, that were not wanted in the first place
    pip_run('uninstall', '--require-virtualenv', '--no-input', '--yes', 'wheel', 'setuptools', 'pip')


if __name__ == '__main__':
    main()
