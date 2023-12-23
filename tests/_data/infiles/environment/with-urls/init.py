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
        'git+https://github.com/pypa/packaging.git@23.2',
        'urllib3 @ https://github.com/urllib3/urllib3/archive/refs/tags/1.26.8.zip',
        'https://files.pythonhosted.org/packages/d9/5a/'
        'e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl',
    )


if __name__ == '__main__':
    main()
