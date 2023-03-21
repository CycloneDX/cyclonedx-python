# encoding: utf-8

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
import os
import sys
from argparse import ArgumentParser, FileType
from typing import Optional

from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import BaseOutput, get_instance as get_output_instance
from cyclonedx.parser import BaseParser
from cyclonedx.schema import OutputFormat, SchemaVersion

from ..exception import CycloneDxCmdException, CycloneDxCmdNoInputFileSupplied
from ..parser._cdx_properties import Pipenv as PipenvProps, Poetry as PoetryProp
from ..parser.conda import CondaListExplicitParser, CondaListJsonParser
from ..parser.environment import EnvironmentParser
from ..parser.pipenv import PipenvPackageCategoryGroupWellknown, PipEnvParser
from ..parser.poetry import PoetryGroupWellknown, PoetryParser
from ..parser.requirements import RequirementsParser
from ..utils.output import CLI_OMITTABLE, CLI_OUTPUT_FORMAT, OUTPUT_DEFAULT_FILENAMES, OUTPUT_FORMATS
from . import BaseCommand, cdx_version


class MakeBomCommand(BaseCommand):

    def handle_args(self) -> int:
        output_format = self._get_output_format()
        self._debug_message('output_format: {}', output_format)

        # Quick check for JSON && SchemaVersion <= 1.1
        if output_format == OutputFormat.JSON and str(self.arguments.output_schema_version) in ['1.0', '1.1']:
            self._error_and_exit(
                'CycloneDX schema does not support JSON output in Schema Versions < 1.2',
                exit_code=2
            )

        output = self.get_output()
        if self.arguments.output_file == '-' or not self.arguments.output_file:
            self._debug_message('Returning SBOM to STDOUT')
            print(output.output_as_string(), file=sys.stdout)
            return 0

        # Check directory writable
        output_file = self.arguments.output_file
        output_filename = os.path.realpath(
            output_file if isinstance(output_file, str) else OUTPUT_DEFAULT_FILENAMES[output_format])
        self._debug_message('Will be outputting SBOM to file at: {}', output_filename)
        output.output_to_file(filename=output_filename, allow_overwrite=self.arguments.output_file_overwrite)

        return 0

    def get_argument_parser_name(self) -> str:
        return 'make-bom'

    def get_argument_parser_help(self) -> str:
        return 'Make a BOM from your environment as specified'

    def setup_argument_parser(self, arg_parser: ArgumentParser) -> None:
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
            description='Flags to determine how this tool obtains it\'s input'
        )
        input_method_group.add_argument(
            '-i', '--in-file', action='store', metavar='FILE_PATH',
            type=FileType('r'),  # FileType does handle '-'
            default=None,
            help='File to read input from. Use "-" to read from STDIN.', dest='input_source', required=False
        )

        output_group = arg_parser.add_argument_group(
            title='SBOM Output Configuration',
            description='Choose the output format and schema version'
        )
        output_group.add_argument(
            '--format', action='store',
            choices=[f.value for f in CLI_OUTPUT_FORMAT], default=CLI_OUTPUT_FORMAT.XML.value,
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
        arg_parser.add_argument(
            "--omit", dest="omit", action="append",
            default=[],
            help=f'Omit specified items when using Poetry or PipEnv (choice: {CLI_OMITTABLE.DevDependencies.value})',
        )

    def get_output(self) -> BaseOutput:
        parser: Optional[BaseParser] = None
        try:
            parser = self._get_input_parser()
        except CycloneDxCmdNoInputFileSupplied as error:
            print(f'ERROR: {str(error)}', file=sys.stderr)
            exit(1)
        except CycloneDxCmdException as error:
            print(f'ERROR: {str(error)}', file=sys.stderr)
            exit(1)

        if not parser:
            self._error_and_exit('No Parser created - check the code!')

        if parser.has_warnings():
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

        bom = Bom(components=filter(self._component_filter, parser.get_components()))
        bom.metadata.tools.add(Tool(
            vendor='CycloneDX',
            name='cyclonedx-bom',
            version=cdx_version
        ))

        return get_output_instance(
            bom=bom,
            output_format=OUTPUT_FORMATS[self._get_output_format()],
            schema_version=SchemaVersion['V{}'.format(
                str(self.arguments.output_schema_version).replace('.', '_')
            )]
        )

    def _get_input_parser(self) -> BaseParser:
        if self.arguments.input_from_environment:
            return EnvironmentParser(
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'EnvironmentParser {m}', *a, **k)
            )

        # All other Parsers will require some input - grab it now!
        if not self.arguments.input_source:
            # Nothing passed via STDIN, and no FILENAME supplied, let's assume a default by input type for ease
            current_directory = os.getcwd()
            try:
                if self.arguments.input_from_conda_explicit:
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda Explicit, you need to pipe input via STDIN')
                elif self.arguments.input_from_conda_json:
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda JSON, you need to pipe input via STDIN')
                elif self.arguments.input_from_pip:
                    self.arguments.input_source = open(os.path.join(current_directory, 'Pipfile.lock'), 'r')
                elif self.arguments.input_from_poetry:
                    self.arguments.input_source = open(os.path.join(current_directory, 'poetry.lock'), 'r')
                elif self.arguments.input_from_requirements:
                    self.arguments.input_source = open(os.path.join(current_directory, 'requirements.txt'), 'r')
                else:
                    raise CycloneDxCmdException('Parser type could not be determined.')
            except FileNotFoundError as error:
                raise CycloneDxCmdNoInputFileSupplied(
                    f'No input file was supplied and no input was provided on STDIN:\n{str(error)}'
                ) from error

        input_data_fh = self.arguments.input_source
        with input_data_fh:
            input_data = input_data_fh.read()
            input_data_fh.close()

        if self.arguments.input_from_conda_explicit:
            return CondaListExplicitParser(
                conda_data=input_data,
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'CondaListExplicitParser {m}', *a, **k)
            )
        elif self.arguments.input_from_conda_json:
            return CondaListJsonParser(
                conda_data=input_data,
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'CondaListJsonParser {m}', *a, **k)
            )
        elif self.arguments.input_from_pip:
            return PipEnvParser(
                pipenv_contents=input_data,
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'PipEnvParser {m}', *a, **k)
            )
        elif self.arguments.input_from_poetry:
            return PoetryParser(
                poetry_lock_contents=input_data,
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'PoetryParser {m}', *a, **k)
            )
        elif self.arguments.input_from_requirements:
            return RequirementsParser(
                requirements_content=input_data,
                use_purl_bom_ref=self.arguments.use_purl_bom_ref,
                debug_message=lambda m, *a, **k: self._debug_message(f'RequirementsParser {m}', *a, **k)
            )
        else:
            raise CycloneDxCmdException('Parser type could not be determined.')

    def _component_filter(self, component: Component) -> bool:
        if CLI_OMITTABLE.DevDependencies.value in self.arguments.omit:
            for prop in component.properties:
                if prop.name == PipenvProps.PackageCategory.value:
                    if prop.value == PipenvPackageCategoryGroupWellknown.Develop.value:
                        return False
                elif prop.name == PoetryProp.PackageGroup.value:
                    if prop.value == PoetryGroupWellknown.Dev.value:
                        return False

        return True

    def _get_output_format(self) -> CLI_OUTPUT_FORMAT:
        return CLI_OUTPUT_FORMAT(str(self.arguments.output_format).lower())
