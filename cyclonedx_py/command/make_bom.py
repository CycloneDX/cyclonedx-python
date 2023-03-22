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
from io import TextIOWrapper
from typing import Iterable, Optional

import click
from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import BaseOutput, get_instance as get_output_instance
from cyclonedx.parser import BaseParser
from cyclonedx.schema import OutputFormat, SchemaVersion

from . import (
    BaseCommand,
    CycloneDxCmd,
    _get_output_format,
    cdx_version,
    cli,
    input_python_options,
    output_cyclonedx_options,
    root_cdx_command,
)
from ..exception import CycloneDxCmdException, CycloneDxCmdNoInputFileSupplied
from ..parser._cdx_properties import Pipenv as PipenvProps, Poetry as PoetryProp
from ..parser.conda import CondaListExplicitParser, CondaListJsonParser
from ..parser.environment import EnvironmentParser
from ..parser.pipenv import PipenvPackageCategoryGroupWellknown, PipEnvParser
from ..parser.poetry import PoetryGroupWellknown, PoetryParser
from ..parser.requirements import RequirementsParser
from ..utils.output import CLI_OMITTABLE, OUTPUT_DEFAULT_FILENAMES, OUTPUT_FORMATS


@cli.command(help='Generate a CycloneDX BOM from a Python Environment or Application')
@root_cdx_command
@input_python_options
@output_cyclonedx_options
def make_bom(cmd: CycloneDxCmd, input_type: str, in_file: TextIOWrapper, o: str,
             output_format: str, schema_version: str, force: bool = False, purl_bom_ref: bool = False,
             omit: Optional[str] = None) -> None:
    c = MakeBomCommand(cmd=cmd, input_type=input_type, in_file=in_file, o=o, output_format=output_format,
                       schema_version=schema_version, force=force, purl_bom_ref=purl_bom_ref, omit=omit or [])
    rc = c.execute()
    if rc > 0 and not cmd.warn_only:
        c.error_and_exit('There were errors or warnings', exit_code=rc)

    return


class MakeBomCommand(BaseCommand):

    def __init__(self, *, cmd: CycloneDxCmd, input_type: str, in_file: TextIOWrapper, o: str,
                 output_format: str, schema_version: str, force: bool = False, purl_bom_ref: bool = False,
                 omit: Iterable[str]) -> None:
        super().__init__(cmd=cmd)
        self.input_type = input_type
        self.in_file = in_file
        self.output = o
        self.output_format = output_format
        self.schema_version = schema_version
        self.force = force
        self.purl_bom_ref = purl_bom_ref
        self.omit = omit

    def execute(self) -> int:
        output_format = _get_output_format(output_format=self.output_format)
        self.debug_message('output_format: {}', self.output_format)

        # Quick check for JSON && SchemaVersion <= 1.1
        if output_format == OutputFormat.JSON and str(self.schema_version) in ['1.0', '1.1']:
            self.error_and_exit(
                'CycloneDX schema does not support JSON output in Schema Versions < 1.2',
                exit_code=2
            )

        input_parser: BaseParser
        try:
            input_parser = self._get_input_parser()
        except CycloneDxCmdException as error:
            self.error_and_exit(message=str(error), exit_code=1)

        if input_parser and input_parser.has_warnings():
            warning_message = '\n'.join(['',
                                         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
                                         '!! Some of your dependencies do not have pinned version !!',
                                         '!! numbers in your requirements.txt                     !!',
                                         '!!                                                      !!',
                                         *('!! -> {} !!'.format(warning.get_item().ljust(49)) for warning in
                                           input_parser.get_warnings()),
                                         '!!                                                      !!',
                                         '!! The above will NOT be included in the generated      !!',
                                         '!! CycloneDX as version is a mandatory field.           !!',
                                         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
                                         ''])
            click.echo(warning_message, file=sys.stderr, err=True)

        bom = Bom(components=filter(self._component_filter, input_parser.get_components()))
        bom.metadata.tools.add(Tool(
            vendor='CycloneDX',
            name='cyclonedx-bom',
            version=cdx_version
        ))

        cdx_outputter: BaseOutput = get_output_instance(
            bom=bom, output_format=OUTPUT_FORMATS[_get_output_format(output_format=self.output_format)],
            schema_version=SchemaVersion['V{}'.format(str(self.schema_version).replace('.', '_'))]
        )

        if self.output == '-' or not self.output:
            self.debug_message('Returning SBOM to STDOUT')
            print(cdx_outputter.output_as_string(), file=sys.stdout)
            return 0

        # Check directory writable
        output_filename = os.path.realpath(
            self.output if isinstance(self.output, str) else OUTPUT_DEFAULT_FILENAMES[output_format])
        self.debug_message('Will be outputting SBOM to file at: {}', self.output)
        try:
            cdx_outputter.output_to_file(filename=output_filename, allow_overwrite=self.force)
        except FileExistsError:
            return self.error_and_exit(f'Requested output file already exists: {output_filename}', exit_code=3)

        return 0

    def _get_input_parser(self) -> BaseParser:
        if self.input_type == 'ENVIRONMENT':
            return EnvironmentParser(
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'EnvironmentParser {m}', *a, **k)
            )

        # All other Parsers will require some input - grab it now!
        self.debug_message('Input is: {}', self.in_file)
        if not self.in_file:
            # Nothing passed via STDIN, and no FILENAME supplied, let's assume a default by input type for ease
            current_directory = os.getcwd()
            try:
                if self.input_type == 'CONDA':
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda Explicit, you need to pipe input via STDIN')
                elif self.input_type == 'CONDA_JSON':
                    raise CycloneDxCmdNoInputFileSupplied(
                        'When using input from Conda JSON, you need to pipe input via STDIN')
                elif self.input_type == 'PIPENV':
                    self.in_file = open(os.path.join(current_directory, 'Pipfile.lock'), 'r')
                elif self.input_type == 'POETRY':
                    self.in_file = open(os.path.join(current_directory, 'poetry.lock'), 'r')
                elif self.input_type == 'REQUIREMENTS':
                    self.in_file = open(os.path.join(current_directory, 'requirements.txt'), 'r')
                else:
                    raise CycloneDxCmdException('Parser type could not be determined.')
            except FileNotFoundError as error:
                raise CycloneDxCmdNoInputFileSupplied(
                    f'No input file was supplied and no input was provided on STDIN:\n{str(error)}'
                ) from error

        with self.in_file:
            input_data = self.in_file.read()

        if self.input_type == 'CONDA':
            return CondaListExplicitParser(
                conda_data=input_data,
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'CondaListExplicitParser {m}', *a, **k)
            )
        elif self.input_type == 'CONDA_JSON':
            return CondaListJsonParser(
                conda_data=input_data,
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'CondaListJsonParser {m}', *a, **k)
            )
        elif self.input_type == 'PIPENV':
            return PipEnvParser(
                pipenv_contents=input_data,
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'PipEnvParser {m}', *a, **k)
            )
        elif self.input_type == 'POETRY':
            return PoetryParser(
                poetry_lock_contents=input_data,
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'PoetryParser {m}', *a, **k)
            )
        elif self.input_type == 'REQUIREMENTS':
            return RequirementsParser(
                requirements_content=input_data,
                use_purl_bom_ref=self.purl_bom_ref,
                debug_message=lambda m, *a, **k: self.debug_message(f'RequirementsParser {m}', *a, **k)
            )
        else:
            raise CycloneDxCmdException('Parser type could not be determined.')

    def _component_filter(self, component: Component) -> bool:
        if CLI_OMITTABLE.DevDependencies.value in self.omit:
            for prop in component.properties:
                if prop.name == PipenvProps.PackageCategory.value:
                    if prop.value == PipenvPackageCategoryGroupWellknown.Develop.value:
                        return False
                elif prop.name == PoetryProp.PackageGroup.value:
                    if prop.value == PoetryGroupWellknown.Dev.value:
                        return False

        return True
