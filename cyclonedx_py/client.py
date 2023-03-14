#!/usr/bin/env python
# encoding: utf-8

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

from argparse import ArgumentParser, Namespace
from typing import Dict, Optional

from .command import BaseCommand, cdx_version
from .command.make_bom import MakeBomCommand

_SUB_COMMANDS: Dict[str, BaseCommand] = {
    'make-bom': MakeBomCommand()
}


class CycloneDxCmd:

    def __init__(self, args: Namespace) -> None:
        self._arguments = args

        if self._arguments.debug_enabled:
            self._debug_enabled = True

    @property
    def debug_enabled(self) -> bool:
        return self._debug_enabled

    def execute(self) -> None:
        # Determine primary command and then hand off to that Command handler
        if self._arguments.cmd and self._arguments.cmd in _SUB_COMMANDS.keys():
            command = _SUB_COMMANDS[self._arguments.cmd]
            exit_code: int = command.execute(arguments=self._arguments)
            exit(exit_code)
        else:
            CycloneDxCmd.get_arg_parser().print_help()

    @staticmethod
    def get_arg_parser(*, prog: Optional[str] = None) -> ArgumentParser:
        arg_parser = ArgumentParser(prog=prog, description='CycloneDX BOM Generator')

        # Add global options
        arg_parser.add_argument('-v', '--version', help='show which version of CycloneDX BOM Generator you are running',
                                action='version',
                                version=f'CycloneDX BOM Generator {cdx_version}')
        arg_parser.add_argument('-w', '--warn-only', action='store_true', dest='warn_only',
                                help='prevents exit with non-zero code when issues have been detected')
        arg_parser.add_argument('-X', action='store_true', help='enable debug output', dest='debug_enabled')

        subparsers = arg_parser.add_subparsers(title='CycloneDX BOM Generator sub-commands', dest='cmd', metavar='')
        for subcommand in _SUB_COMMANDS.keys():
            _SUB_COMMANDS[subcommand].setup_argument_parser(
                arg_parser=subparsers.add_parser(
                    name=_SUB_COMMANDS[subcommand].get_argument_parser_name(),
                    help=_SUB_COMMANDS[subcommand].get_argument_parser_help()
                )
            )

        return arg_parser


def main(*, prog_name: Optional[str] = None) -> None:
    parser = CycloneDxCmd.get_arg_parser(prog=prog_name)
    args = parser.parse_args()
    CycloneDxCmd(args=args).execute()


if __name__ == "__main__":
    main()
