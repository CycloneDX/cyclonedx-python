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
import os
import sys
from datetime import datetime

from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.output import BaseOutput, get_instance, OutputFormat, SchemaVersion
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
            self._debug_message('Parsed Arguments: {}'.format(self._arguments))

    def get_output(self) -> BaseOutput:
        try:
            parser = self._get_input_parser()
        except CycloneDxCmdNoInputFileSupplied as e:
            print(f'ERROR: {str(e)}')
            exit(1)
        except CycloneDxCmdException as e:
            print(f'ERROR: {str(e)}')
            exit(1)

        if parser and parser.has_warnings():
            print('')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!! Some of your dependencies do not have pinned version !!')
            print('!! numbers in your requirements.txt                     !!')
            print('!!                                                      !!')
            for warning in parser.get_warnings():
                print('!! -> {} !!'.format(warning.get_item().ljust(49)))
            print('!!                                                      !!')
            print('!! The above will NOT be included in the generated      !!')
            print('!! CycloneDX as version is a mandatory field.           !!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('')

        bom = Bom.from_parser(parser=parser)

        # Add cyclonedx_bom as a Tool to record it being part of the CycloneDX SBOM generation process
        if sys.version_info >= (3, 8, 0):
            from importlib.metadata import version as md_version
        else:
            from importlib_metadata import version as md_version  # type: ignore
        bom.metadata.tools.add(Tool(
            vendor='CycloneDX', name='cyclonedx-bom', version=md_version('cyclonedx-bom')
        ))

        return get_instance(
            bom=bom,
            output_format=OutputFormat[str(self._arguments.output_format).upper()],
            schema_version=SchemaVersion['V{}'.format(
                str(self._arguments.output_schema_version).replace('.', '_')
            )]
        )

    def execute(self) -> None:
        # Quick check for JSON && SchemaVersion <= 1.1
        if str(self._arguments.output_format).upper() == 'JSON' and \
                str(self._arguments.output_schema_version) in ['1.0', '1.1']:
            self._error_and_exit(
                message='CycloneDX schema does not support JSON output in Schema Versions < 1.2',
                exit_code=2
            )

        output = self.get_output()
        if self._arguments.output_file == '-' or not self._arguments.output_file:
            self._debug_message('Returning SBOM to STDOUT')
            print(output.output_as_string())
            return

        # Check directory writable
        output_filename = os.path.realpath(self._arguments.output_file)
        self._debug_message('Will be outputting SBOM to file at: {}'.format(output_filename))
        output.output_to_file(filename=output_filename, allow_overwrite=self._arguments.output_file_overwrite)

    @staticmethod
    def get_arg_parser() -> argparse.ArgumentParser:
        arg_parser = argparse.ArgumentParser(description='CycloneDX SBOM Generator')

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
            help='Build a SBOM based on a Poetry poetry.lock\'s contents. Use with -i to specify absolute path'
                 'to a `poetry.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_poetry'
        )
        input_group.add_argument(
            '-pip', '--pip', action='store_true',
            help='Build a SBOM based on a PipEnv Pipfile.lock\'s contents. Use with -i to specify absolute path'
                 'to a `Pipefile.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_pip'
        )
        input_group.add_argument(
            '-r', '--r', '--requirements', action='store_true',
            help='Build a SBOM based on a requirements.txt\'s contents. Use with -i to specify absolute path'
                 'to a `requirements.txt` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_requirements'
        )

        input_method_group = arg_parser.add_argument_group(
            title='Input Method',
            description='Flags to determine how `cyclonedx-bom` obtains it\'s input'
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
            '--format', action='store', choices=['json', 'xml'], default='xml',
            help='The output format for your SBOM (default: %(default)s)',
            dest='output_format'
        )
        output_group.add_argument(
            '--schema-version', action='store', choices=['1.4', '1.3', '1.2', '1.1', '1.0'], default='1.4',
            help='The CycloneDX schema version for your SBOM (default: %(default)s)',
            dest='output_schema_version'
        )
        output_group.add_argument(
            '-o', '--o', '--output', action='store', metavar='FILE_PATH', default='cyclonedx.xml', required=False,
            help='Output file path for your SBOM (set to \'-\' to output to STDOUT)', dest='output_file'
        )
        output_group.add_argument(
            '-F', '--force', action='store_true', dest='output_file_overwrite',
            help='If outputting to a file and the stated file already exists, it will be overwritten.'
        )

        arg_parser.add_argument('-X', action='store_true', help='Enable debug output', dest='debug_enabled')

        return arg_parser

    def _debug_message(self, message: str) -> None:
        if self._DEBUG_ENABLED:
            print('[DEBUG] - {} - {}'.format(datetime.now(), message))

    @staticmethod
    def _error_and_exit(message: str, exit_code: int = 1) -> None:
        print('[ERROR] - {} - {}'.format(datetime.now(), message))
        exit(exit_code)

    def _get_input_parser(self) -> BaseParser:
        if self._arguments.input_from_environment:
            return EnvironmentParser()

        # All other Parsers will require some input - grab it now!
        if not self._arguments.input_source:
            # Nothing passed via STDIN, and no FILENAME supplied, let's assume a default by input type for ease
            current_directory = os.getcwd()
            try:
                if self._arguments.input_from_conda_explicit:
                    raise CycloneDxCmdNoInputFileSupplied('When using input from Conda Explicit, you need to pipe input'
                                                          'via STDIN')
                elif self._arguments.input_from_conda_json:
                    raise CycloneDxCmdNoInputFileSupplied('When using input from Conda JSON, you need to pipe input'
                                                          'via STDIN')
                elif self._arguments.input_from_pip:
                    self._arguments.input_source = open(os.path.join(current_directory, 'Pipfile.lock'), 'r')
                elif self._arguments.input_from_poetry:
                    self._arguments.input_source = open(os.path.join(current_directory, 'poetry.lock'), 'r')
                elif self._arguments.input_from_requirements:
                    self._arguments.input_source = open(os.path.join(current_directory, 'requirements.txt'), 'r')
                else:
                    raise CycloneDxCmdException('Parser type could not be determined.')
            except FileNotFoundError as e:
                raise CycloneDxCmdNoInputFileSupplied(
                    f'No input file was supplied and no input was provided on STDIN:\n{str(e)}'
                )

        input_data_fh = self._arguments.input_source
        with input_data_fh:
            input_data = input_data_fh.read()
            input_data_fh.close()

        if self._arguments.input_from_conda_explicit:
            return CondaListExplicitParser(conda_data=input_data)
        elif self._arguments.input_from_conda_json:
            return CondaListJsonParser(conda_data=input_data)
        elif self._arguments.input_from_pip:
            return PipEnvParser(pipenv_contents=input_data)
        elif self._arguments.input_from_poetry:
            return PoetryParser(poetry_lock_contents=input_data)
        elif self._arguments.input_from_requirements:
            return RequirementsParser(requirements_content=input_data)
        else:
            raise CycloneDxCmdException('Parser type could not be determined.')


def main() -> None:
    parser = CycloneDxCmd.get_arg_parser()
    args = parser.parse_args()
    CycloneDxCmd(args).execute()


if __name__ == "__main__":
    main()
