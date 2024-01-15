"""
initialize this testbed.
"""

from os import environ
from os.path import dirname, join
from shutil import rmtree
from subprocess import CompletedProcess, run  # nosec:B404
from sys import executable

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')

pdm_env = environ.copy()
pdm_env['PDM_IGNORE_ACTIVE_VENV'] = '1'
pdm_env.pop('PDM_IGNORE_SAVED_PYTHON', None)


def pdm_run(*args: str) -> CompletedProcess:
    # PDM is not API, but a CLI -- call it like that!
    call = (
        executable, '-m', 'pdm',
        *args
    )
    print('+ ', *call)
    res = run(call, cwd=this_dir, env=pdm_env, shell=False)  # nosec:B603
    if res.returncode != 0:
        raise RuntimeError('process failed')
    return res


def main() -> None:
    # needed to reinit partially stripped evn
    rmtree(env_dir, ignore_errors=True)

    # the actual setuo
    pdm_run('venv', 'create', '--force')
    pdm_run('use', env_dir)  # needed since this whole process might be running in a different venv itself
    pdm_run('install', '--prod')


if __name__ == '__main__':
    main()
