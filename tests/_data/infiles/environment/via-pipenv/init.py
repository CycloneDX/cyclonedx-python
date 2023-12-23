"""
initialize this testbed.
"""

from os.path import dirname, join
from shutil import rmtree
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')


def pipenv_run(*args: str) -> CompletedProcess:
    # pipenv is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pipenv',
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, env={
        'PIPENV_VENV_IN_PROJECT': '1',
        'PIPENV_IGNORE_VIRTUALENVS': '1',
        'PIPENV_NO_INHERIT': '1',
        'PIPENV_NOSPIN': '1',
        'PATH': '',  # existence is required for strange reasons
    }, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def main() -> None:

    rmtree(env_dir, ignore_errors=True)  # needed to reinit partially stripped evn
    pipenv_run('install', '--deploy', '--no-site-packages')
    # uninstall things that were coming with virtualenv, that were not wanted in the first place
    pipenv_run('run', 'pip', 'uninstall', '--yes', 'wheel', 'setuptools', 'pip')


if __name__ == '__main__':
    main()
