"""
initialize this testbed.
"""

from os.path import dirname
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable

__all__ = ['main']

this_dir = dirname(__file__)


def poetry_run(*args: str) -> CompletedProcess:
    # Poetry is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'poetry',
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, env={}, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def main() -> None:
    poetry_run('install', '--no-dev', '--no-interaction', '--sync')


if __name__ == '__main__':
    main()
