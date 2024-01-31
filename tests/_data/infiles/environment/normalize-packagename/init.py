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
        # https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization
        'ruamel-YAML[jinja2]',  # actually "ruamel.yaml", normalizes to "ruamel-yaml"
    )


if __name__ == '__main__':
    main()
    if '--pin' in argv:
        res = pip_run('freeze', '--all', '--local', stdout=PIPE)
        with open(constraint_file, 'wb') as cf:
            cf.write(res.stdout)
