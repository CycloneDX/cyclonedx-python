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

from importlib.util import module_from_spec, spec_from_file_location
from os import name as os_name
from os.path import dirname, join
from random import randrange
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable, stderr
from threading import Thread
from time import sleep
from typing import TYPE_CHECKING, Callable
from venv import EnvBuilder

if TYPE_CHECKING:
    from http.server import ThreadingHTTPServer

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')

__proxy_spec = spec_from_file_location('pypi_proxy', join(dirname(__file__), '..', '..', '_helpers', 'pypi-proxy.py'))
__proxy_module = module_from_spec(__proxy_spec)
__proxy_spec.loader.exec_module(__proxy_module)
make_proxy: Callable[[int], 'ThreadingHTTPServer'] = __proxy_module.make_proxy
del __proxy_spec, __proxy_module


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
    _retries = 5
    while True:
        # use the range of "dynamic unregistered for temporary usage"
        _port = randrange(49152, 65535)  # nosec:B311
        try:
            proxy = make_proxy(_port)
        except Exception as error:
            print(f'failed attempt to open proxy on port {_port}:', error, file=stderr)
        else:
            break
        if _retries > 0:
            _retries -= 1
            print('will retry in 1 second', file=stderr)
            sleep(1)
        else:
            raise RuntimeError('failed to setup proxy')

    proxy_threat = Thread(target=proxy.serve_forever)
    proxy_threat.start()
    print(f'running PyPI proxy at: {proxy.server_address!r}', file=stderr)

    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)

    pip_install(
        'https://user:password@files.pythonhosted.org/packages/d9/5a/'
        'e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl',
    )

    pip_install(
        '--index-url', f'http://user:password@127.0.0.1:{proxy.server_port}/simple',
        'toml==0.10.2'
    )

    proxy.shutdown()
    print(f'closed PyPI proxy at: {proxy.server_address!r}', file=stderr)


if __name__ == '__main__':
    main()
