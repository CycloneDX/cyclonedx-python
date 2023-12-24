"""
initialize this testbed.
"""

from os import name as os_name
from os.path import dirname, join
from venv import EnvBuilder

__all__ = ['main']

env_dir = join(dirname(__file__), '.venv')


def main() -> None:
    EnvBuilder(
        system_site_packages=False,
        symlinks=os_name != 'nt',
        with_pip=False,
    ).create(env_dir)


if __name__ == '__main__':
    main()
