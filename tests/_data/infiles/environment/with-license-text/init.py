"""
initialize this testbed.
"""

from os import name as os_name
from os.path import abspath, dirname, join
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable
from typing import Any
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')
constraint_file = join(this_dir, 'pinning.txt')

localpackages_dir = abspath(join(dirname(__file__), '..', '..', '_helpers', 'local_pckages'))


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
        *args
    )


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)

    pip_install(
        join(localpackages_dir, 'a', 'dist', 'package_a-23.42-py3-none-any.whl'),
        join(localpackages_dir, 'b', 'dist', 'package_b-23.42-py3-none-any.whl'),
        join(localpackages_dir, 'c', 'dist', 'package_c-23.42-py3-none-any.whl'),
    )


if __name__ == '__main__':
    main()
