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

from cyclonedx.model.bom import Bom, Tool
from cyclonedx.output import BaseOutput, get_instance, OutputFormat, SchemaVersion
from cyclonedx.parser import BaseParser
from cyclonedx.parser.environment import EnvironmentParser
from cyclonedx.parser.pipenv import PipEnvFileParser
from cyclonedx.parser.poetry import PoetryFileParser
from cyclonedx.parser.requirements import RequirementsFileParser


class CycloneDxCmd:
    # Whether debug output is enabled
    _DEBUG_ENABLED: bool = False

    # Parsed Arguments
    _arguments: argparse.Namespace

    def __init__(self, args: argparse.Namespace):
        self._arguments = args

        if self._arguments.debug_enabled:
            self._DEBUG_ENABLED = True
            self._debug_message('!!! DEBUG MODE ENABLED !!!')
            self._debug_message('Parsed Arguments: {}'.format(self._arguments))

    def get_output(self) -> BaseOutput:
        parser = self._get_input_parser()

        if parser.has_warnings():
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
            from importlib.metadata import version
        else:
            from importlib_metadata import version
        bom.get_metadata().add_tool(tool=Tool(
            vendor='CycloneDX', name='cyclonedx-bom', version=version('cyclonedx-bom')
        ))

        return get_instance(
            bom=bom,
            output_format=OutputFormat[str(self._arguments.output_format).upper()],
            schema_version=SchemaVersion['V{}'.format(
                str(self._arguments.output_schema_version).replace('.', '_')
            )]
        )

    def execute(self):
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
            '-e', '--e', '--environment', action='store_true',
            help='Build a SBOM based on the packages installed in your current Python environment (default)',
            dest='input_from_environment'
        )
        input_group.add_argument(
            '-p', '--p', '--poetry', action='store_true',
            help='Build a SBOM based on a Poetry poetry.lock\'s contents. Use with -pf to specify absolute path'
                 'to a `poetry.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_poetry'
        )
        input_group.add_argument(
            '-pip', '--pip', action='store_true',
            help='Build a SBOM based on a PipEnv Pipfile.lock\'s contents. Use with --pip-file to specify absolute path'
                 'to a `Pipefile.lock` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_pip'
        )
        input_group.add_argument(
            '-r', '--r', '--requirements', action='store_true',
            help='Build a SBOM based on a requirements.txt\'s contents. Use with -rf to specify absolute path'
                 'to a `requirements.txt` you wish to use, else we\'ll look for one in the current working directory.',
            dest='input_from_requirements'
        )

        req_input_group = arg_parser.add_argument_group(
            title='Poetry',
            description='Additional optional arguments if you are setting the input type to `poetry`'
        )
        req_input_group.add_argument(
            '-pf', '--pf', '--poetry-file', action='store', metavar='FILE_PATH', default='poetry.lock',
            help='Path to a the `poetry.lock` file you wish to parse',
            dest='input_poetry_file', required=False
        )

        req_input_group = arg_parser.add_argument_group(
            title='PipEnv',
            description='Additional optional arguments if you are setting the input type to `pipenv`'
        )
        req_input_group.add_argument(
            '--pip-file', action='store', metavar='FILE_PATH', default='Pipfile.lock',
            help='Path to a the `Pipfile.lock` file you wish to parse',
            dest='input_pipenv_file', required=False
        )

        req_input_group = arg_parser.add_argument_group(
            title='Requirements',
            description='Additional optional arguments if you are setting the input type to `requirements`.'
        )
        req_input_group.add_argument(
            '-rf', '--rf', '--requirements-file', action='store', metavar='FILE_PATH', default='requirements.txt',
            help='Path to a the `requirements.txt` file you wish to parse',
            dest='input_requirements_file', required=False
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
            '--schema-version', action='store', choices=['1.3', '1.2', '1.1', '1.0'], default='1.3',
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

    def _debug_message(self, message: str):
        if self._DEBUG_ENABLED:
            print('[DEBUG] - {} - {}'.format(datetime.now(), message))

    @staticmethod
    def _error_and_exit(message: str, exit_code: int = 1):
        print('[ERROR] - {} - {}'.format(datetime.now(), message))
        exit(exit_code)

    def _get_input_parser(self) -> BaseParser:
        if self._arguments.input_from_environment:
            return EnvironmentParser()
        elif self._arguments.input_from_pip:
            pipfile_lock_file = os.path.realpath(self._arguments.input_pipenv_file)
            if CycloneDxCmd._validate_file_exists(self._arguments.input_pipenv_file):
                # A Pipfile.lock path was provided
                return PipEnvFileParser(pipenv_lock_filename=pipfile_lock_file)
            else:
                self._error_and_exit(f'The provided file \'{pipfile_lock_file}\' does not exist')
        elif self._arguments.input_from_poetry:
            poetry_lock_file = os.path.realpath(self._arguments.input_poetry_file)
            if CycloneDxCmd._validate_file_exists(self._arguments.input_poetry_file):
                # A poetry.lock path was provided
                return PoetryFileParser(poetry_lock_filename=poetry_lock_file)
            else:
                self._error_and_exit('The provided file \'{}\' does not exist'.format(
                    poetry_lock_file
                ))
        elif self._arguments.input_from_requirements:
            requirements_file = os.path.realpath(self._arguments.input_requirements_file)
            if CycloneDxCmd._validate_file_exists(self._arguments.input_requirements_file):
                # A requirements.txt path was provided
                return RequirementsFileParser(requirements_file=requirements_file)
            else:
                self._error_and_exit('The provided file \'{}\' does not exist'.format(
                    requirements_file
                ))
        else:
            raise ValueError('Parser type could not be determined.')

    @staticmethod
    def _validate_file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)


def main():
    parser = CycloneDxCmd.get_arg_parser()
    args = parser.parse_args()
    CycloneDxCmd(args).execute()


if __name__ == "__main__":
    main()
