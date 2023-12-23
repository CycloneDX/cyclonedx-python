from typing import TYPE_CHECKING

from .utils.args import argparse_type4enum

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Action, ArgumentParser


def add_argument_pyproject(p: 'ArgumentParser') -> 'Action':
    return p.add_argument('--pyproject',
                          metavar='FILE',
                          help="Path to the root component's `pyproject.toml` file. "
                               'This should point to a file compliant with PEP 621 '
                               '(storing project metadata).',
                          dest='pyproject_file',
                          default=None)


def add_argument_mc_type(p: 'ArgumentParser') -> 'Action':
    from cyclonedx.model.component import ComponentType
    choices = [ComponentType.APPLICATION,
               ComponentType.FIRMWARE,
               ComponentType.LIBRARY]
    return p.add_argument('--mc-type',
                          metavar='TYPE',
                          help='Type of the main component'
                               f' {{choices: {", ".join(t.value for t in choices)}}}'
                               ' (default: %(default)s)',
                          dest='mc_type',
                          choices=choices,
                          type=argparse_type4enum(ComponentType),
                          default=ComponentType.APPLICATION)
