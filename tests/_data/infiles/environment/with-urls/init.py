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
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')


def pip_run(*args: str) -> CompletedProcess:
    # pip is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pip',
        '--python', env_dir,
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def pip_install(*args: str) -> None:
    pip_run(
        'install', '--require-virtualenv', '--no-input', '--progress-bar=off', '--no-color',
        *args
    )


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)

    pip_install(
        # VCS
        'git+https://github.com/pypa/packaging.git@23.2',
        # named from archive
        'urllib3 @ https://github.com/urllib3/urllib3/archive/refs/tags/2.2.0.zip',
        # unnamed wheel
        'https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/'
        'six-1.16.0-py2.py3-none-any.whl',
        # sdist with hash
        'https://files.pythonhosted.org/packages/c0/3f/d7af728f075fb08564c5949a9c95e44352e23dee646869fa104a3b2060a3/'
        'tomli-2.0.1.tar.gz#sha256:de526c12914f0c550d15924c62d72abc48d6fe7364aa87328337a31007fe8a4f'
    )


if __name__ == '__main__':
    main()
