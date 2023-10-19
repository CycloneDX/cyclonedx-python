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

import argparse
import enum
import os
import sys
from datetime import datetime
from typing import Any, Optional

from chardet import detect as chardetect  # type:ignore[import]
from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.output import BaseOutput, OutputFormat, SchemaVersion, get_instance as get_output_instance
from cyclonedx.parser import BaseParser

from .parser.conda import CondaListExplicitParser, CondaListJsonParser
from .parser.environment import EnvironmentParser
from .parser.pipenv import PipEnvParser
from .parser.poetry import PoetryParser
from .parser.requirements import RequirementsParser


class CycloneDxCmdException(Exception):
    pass


class CycloneDxCmdNoInputFileSupplied(CycloneDxCmdException):
    pass


@enum.unique
class _CLI_OUTPUT_FORMAT(enum.Enum):
    XML = 'xml'
    JSON = 'json'


_output_formats = {
    _CLI_OUTPUT_FORMAT.XML: OutputFormat.XML,
    _CLI_OUTPUT_FORMAT.JSON: OutputFormat.JSON,
}
_output_default_filenames = {
    _CLI_OUTPUT_FORMAT.XML: 'cyclonedx.xml',
    _CLI_OUTPUT_FORMAT.JSON: 'cyclonedx.json',
}


class CycloneDxCmd:
    # Whether debug output is enabled
    _DEBUG_ENABLED: bool = False

    # Parsed Arguments
    _arguments: argparse.Namespace

    def __init__(self, args: argparse.Namespace) -> None:
        self._arguments = args

        if self._arguments.debug_enabled:
            self._DEBUG_ENABLED = True
            self._debug_message('!!! DEBUG MODE ENABLED !!!')
            self._debug_message('Parsed Arguments: {}', self._arguments)

    def _get_output_format(self) -> _CLI_OUTPUT_FORMAT:
        return _CLI_OUTPUT_FORMAT(str(self._arguments.output_format).lower())

    def get_output(self) -> BaseOutput:
        try:
            parser = self._get_input_parser()
        except CycloneDxCmdNoInputFileSupplied as error:
            print(f'ERROR: {str(error)}', file=sys.stderr)
            exit(1)
        except CycloneDxCmdException as error:
            print(f'ERROR: {str(error)}', file=sys.stderr)
            exit(1)

        if parser and parser.has_warnings():
            print('',
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
                  '!! Some of your dependencies do not have pinned version !!',
                  '!! numbers in your requirements.txt                     !!',
                  '!!                                                      !!',
                  *('!! -> {} !!'.format(warning.get_item().ljust(49)) for warning in parser.get_warnings()),
                  '!!                                                      !!',
                  '!! The above will NOT be included in the generated      !!',
                  '!! CycloneDX as version is a mandatory field.           !!',
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
                  '',
                  sep='\n', file=sys.stderr)

        bom = Bom.from_parser(parser=parser)

        # region Add cyclonedx_bom as a Tool to record it being part of the CycloneDX SBOM generation process
        if sys.version_info < (3, 8):
            from typing import Callable

            from importlib_metadata import version as __md_version

            # this stupid kind of code is needed to satisfy mypy/typing
            _md_version: Callable[[str], str] = __md_version
        else:
            from importlib.metadata import version as _md_version
        _this_tool_name = 'cyclonedx-bom'
        _this_tool_version: Optional[str] = _md_version(_this_tool_name)
        bom.metadata.tools.add(Tool(
            vendor='CycloneDX',
            name=_this_tool_name,
            version=_this_tool_version
        ))
        # endregion

        return get_output_instance(
            bom=bom,
            output_format=_output_formats[self._get_output_format()],
            schema_version=SchemaVersion['V{}'.format(
                str(self._arguments.output_schema_version).replace('.', '_')
            )]
        )

    def execute(self) -> None:
        output_format = self._get_output_format()
        self._debug_message('output_format: {}', output_format)

        # Quick check for JSON && SchemaVersion <= 1.1
        if output_format == OutputFormat.JSON and \
                str(self._arguments.output_schema_version) in ['1.0', '1.1']:
            self._error_and_exit(
                'CycloneDX schema does not support JSON output in Schema Versions < 1.2',
                exit_code=2
            )

        output = self.get_output()
        if self._arguments.output_file == '-' or not self._arguments.output_file:
            self._debug_message('Returning SBOM to STDOUT')
            print(output.output_as_string(), file=sys.stdout)
            return

        # Check directory writable
        output_file = self._arguments.output_file
        output_filename = os.path.realpath(
            output_file if isinstance(output_file, str) else _output_default_filenames[output_format])
        self._debug_message('Will be outputting SBOM to file at: {}', output_filename)
        output.output_to_file(filename=output_filename, allow_overwrite=self._arguments.output_file_overwrite)

    @staticmethod
    def get_arg_parser(*, prog: Optional[str] = None) -> argparse.ArgumentParser:
        arg_parser = argparse.ArgumentParser(prog=prog, description='CycloneDX SBOM Generator')

        input_group = arg_parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument(
            '-c', '--conda', action='store_true',
            help='Build a SBOM based on the output from `conda list --explicit` or `conda list --explicit --md5`',
            dest='input_from_conda_explicit'
        )
        input_group.add_argument(
            '-cj', '--conda-json', action='store_true',
            help='Build a SBOM based on the output from `conda list --json`',
            dest='input_from_conda_json'
        )
        input_group.add_argument(
            '-e', '--e', '--environment', action='store_true',
            help='Build a SBOM based on the packages installed in your current Python environment (default)',
            dest='input_from_environment'
        )
        input_group.add_argument(
            '-p', '--p', '--poetry', action='store_true',
            help='Build a SBOM based on a Poetry poetry.lock\'s contents. Use with -i to specify absolute path '
                 'to a `poetry.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_poetry'
        )
        input_group.add_argument(
            '-pip', '--pip', action='store_true',
            help='Build a SBOM based on a PipEnv Pipfile.lock\'s contents. Use with -i to specify absolute path '
                 'to a `Pipfile.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_pip'
        )
        input_group.add_argument(
            '-r', '--r', '--requirements', action='store_true',
            help='Build a SBOM based on a requirements.txt\'s contents. Use with -i to specify absolute path '
                 'to a `requirements.txt` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_requirements'
        )

        input_method_group = arg_parser.add_argument_group(
            title='Input Method',
            description='Flags to determine how this tool obtains its input'
        )
        input_method_group.add_argument(
            '-i', '--in-file', action='store', metavar='FILE_PATH',
            type=argparse.FileType('r'),  # FileType does handle '-'
            default=None,
            help='File to read input from. Use "-" to read from STDIN.', dest='input_source', required=False
        )

        output_group = arg_parser.add_argument_group(
            title='SBOM Output Configuration',
            description='Choose the output format and schema version'
        )
        output_group.add_argument(
            '--format', action='store',
            choices=[f.value for f in _CLI_OUTPUT_FORMAT], default=_CLI_OUTPUT_FORMAT.XML.value,
            help='The output format for your SBOM (default: %(default)s)',
            dest='output_format'
        )
        output_group.add_argument(
            '--schema-version', action='store', choices=['1.4', '1.3', '1.2', '1.1', '1.0'], default='1.4',
            help='The CycloneDX schema version for your SBOM (default: %(default)s)',
            dest='output_schema_version'
        )
        output_group.add_argument(
            # string, None or True. True=autodetect(based-on-format)
            '-o', '--o', '--output', action='store', metavar='FILE_PATH', default=True, required=False,
            help='Output file path for your SBOM (set to \'-\' to output to STDOUT)', dest='output_file'
        )
        output_group.add_argument(
            '-F', '--force', action='store_true', dest='output_file_overwrite',
            help='If outputting to a file and the stated file already exists, it will be overwritten.'
        )
        output_group.add_argument(
            '-pb', '--purl-bom-ref', action='store_true', dest='use_purl_bom_ref',
            help="Use a component's PURL for the bom-ref value, instead of a random UUID"
        )

        arg_parser.add_argument('-X', action='store_true', help='Enable debug output', dest='debug_enabled')

        return arg_parser

    def _debug_message(self, message: str, *args: Any, **kwargs: Any) -> None:
        if self._DEBUG_ENABLED:
            print(f'[DEBUG] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()),
                  file=sys.stderr)

    @staticmethod
    def _error_and_exit(message: str, *args: Any, exit_code: int = 1, **kwargs: Any) -> None:
        print(f'[ERROR] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()),
              file=sys.stderr)
        exit(exit_code)

    def _get_input_parser(self) -> BaseParser:
        if self._arguments.input_from_environment:
            return EnvironmentParser(
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'EnvironmentParser {m}', *a, **k)
            )

        # All other Parsers will require some input - grab it now!
        if not self._arguments.input_source:
            # Nothing passed via STDIN, and no FILENAME supplied, let's assume a default by input type for ease
            current_directory = os.getcwd()
            try:
                if self._arguments.input_from_conda_explicit:
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda Explicit, you need to pipe input via STDIN')
                elif self._arguments.input_from_conda_json:
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda JSON, you need to pipe input via STDIN')
                elif self._arguments.input_from_pip:
                    self._arguments.input_source = open(os.path.join(current_directory, 'Pipfile.lock'),
                                                        'rt', encoding="UTF-8")
                elif self._arguments.input_from_poetry:
                    self._arguments.input_source = open(os.path.join(current_directory, 'poetry.lock'),
                                                        'rt', encoding="UTF-8")
                elif self._arguments.input_from_requirements:
                    self._arguments.input_source = open(os.path.join(current_directory, 'requirements.txt'), 'rb')
                else:
                    raise CycloneDxCmdException('Parser type could not be determined.')
            except FileNotFoundError as error:
                raise CycloneDxCmdNoInputFileSupplied(
                    f'No input file was supplied and no input was provided on STDIN:\n{str(error)}'
                ) from error

        input_data_fh = self._arguments.input_source
        with input_data_fh:
            input_data = input_data_fh.read()
            if isinstance(input_data, bytes):
                input_encoding = (chardetect(input_data)['encoding'] or '').replace(
                    # replace Windows-encoding with code-page
                    'Windows-', 'cp')
                input_data = input_data.decode(input_encoding)
            input_data_fh.close()

        if self._arguments.input_from_conda_explicit:
            return CondaListExplicitParser(
                conda_data=input_data,
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'CondaListExplicitParser {m}', *a, **k)
            )
        elif self._arguments.input_from_conda_json:
            return CondaListJsonParser(
                conda_data=input_data,
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'CondaListJsonParser {m}', *a, **k)
            )
        elif self._arguments.input_from_pip:
            return PipEnvParser(
                pipenv_contents=input_data,
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'PipEnvParser {m}', *a, **k)
            )
        elif self._arguments.input_from_poetry:
            return PoetryParser(
                poetry_lock_contents=input_data,
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'PoetryParser {m}', *a, **k)
            )
        elif self._arguments.input_from_requirements:
            return RequirementsParser(
                requirements_content=input_data,
                use_purl_bom_ref=self._arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'RequirementsParser {m}', *a, **k)
            )
        else:
            raise CycloneDxCmdException('Parser type could not be determined.')


def main(*, prog_name: Optional[str] = None, prog_name_instead: Optional[str] = None) -> None:
    parser = CycloneDxCmd.get_arg_parser(prog=prog_name)
    if prog_name_instead:
        print('',
              '!!! DEPRECATION WARNING !!!',
              f'! The used call method "{parser.prog}" is deprecated.',
              f'! Use "{prog_name_instead}" instead.',
              '',
              sep='\n', file=sys.stderr)
    args = parser.parse_args()
    CycloneDxCmd(args).execute()


def main_deprecated(*, prog_name: Optional[str] = None) -> None:
    main(prog_name=prog_name, prog_name_instead='cyclonedx-py')


if __name__ == "__main__":
    main()
