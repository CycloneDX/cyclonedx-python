"""
initialize this testbed.
"""

from os import name as os_name
from os.path import dirname, join
from venv import EnvBuilder

__all__ = ['main']

this_dir = dirname(__file__)
env_dir = join(this_dir, '.venv')


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)


if __name__ == '__main__':
    main()
