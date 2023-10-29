# This file is part of CycloneDX Python Lib
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

import sys
from argparse import ArgumentParser, ArgumentTypeError, FileType, RawDescriptionHelpFormatter
from typing import TYPE_CHECKING, Any, Dict, Optional, TextIO, Type

from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator

from .. import __version__
from .requirements import RequirementsBB

if TYPE_CHECKING:
    from argparse import Action
    from logging import Logger

    from cyclonedx.model.bom import Bom

    from . import BomBuilder

    BooleanOptionalAction: Optional[Type[Action]]

if sys.version_info >= (3, 9):
    from argparse import BooleanOptionalAction
else:
    BooleanOptionalAction = None


class Command:
    @staticmethod
    def _mk_OutputFormatCI(value: str) -> OutputFormat:
        try:
            return OutputFormat[value.upper()]
        except KeyError:
            raise ArgumentTypeError(f'unsupported value {value!r}')

    @classmethod
    def make_argument_parser(cls, sco: ArgumentParser, **kwargs: Any) -> ArgumentParser:
        p = ArgumentParser(
            description='Creates CycloneDX Software Bill of Materials (SBOM) from Python projects and environments.',
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
            **kwargs)
        p.add_argument('--version', action='version', version=__version__)
        sp = p.add_subparsers(metavar='command', dest='command',
                              # not required. if omitted: show help and exit
                              required=False)

        op = ArgumentParser(add_help=False)
        op.add_argument('-o', '--outfile',
                        help='Output file path for your SBOM (set to "-" to output to STDOUT) (default: %(default)s)',
                        dest='outfile',
                        type=FileType('w', encoding='utf8'),
                        default='-')
        op.add_argument('--sv', '--schema-version',
                        help='The CycloneDX schema version for your SBOM'
                             f' {{choice: {", ".join(sorted((v.to_version() for v in SchemaVersion), reverse=True))}}}'
                             ' (default: %(default)s)',
                        metavar='VERSION',
                        dest='schema_version',
                        choices=SchemaVersion,
                        type=SchemaVersion.from_version,
                        default=SchemaVersion.V1_4.to_version())
        op.add_argument('--of', '--output-format',
                        help='The output format for your SBOM'
                             f' {{choice: {", ".join(sorted(f.name for f in OutputFormat))}}}'
                             ' (default: %(default)s)',
                        metavar='FORMAT',
                        dest='output_format',
                        choices=OutputFormat,
                        type=cls._mk_OutputFormatCI,
                        default=OutputFormat.JSON.name)
        if BooleanOptionalAction:
            op.add_argument('--validate',
                            help='Whether validate the result before outputting (default: %(default)s)',
                            dest='validate',
                            action=BooleanOptionalAction,
                            default=True)
        else:
            vg = op.add_mutually_exclusive_group()
            vg.add_argument('--validate',
                            help='Validate the result before outputting (default: %(default)s)',
                            dest='validate',
                            action='store_true',
                            default=True)
            vg.add_argument('--no-validate',
                            help='Do not validate the result before outputting',
                            dest='validate',
                            action='store_false')

        for sct, scc, scd in (
            ('requirements', RequirementsBB, 'HELP TODO'),
        ):
            spp = scc.make_argument_parser(add_help=False)
            sp.add_parser(sct,
                          help=scd,
                          description=spp.description,
                          epilog=spp.epilog,
                          parents=[spp, op, sco],
                          formatter_class=p.formatter_class,
                          allow_abbrev=p.allow_abbrev,
                          ).set_defaults(bbc=scc)

        return p

    __OWN_ARGS = {'outfile', 'schema_version', 'output_format', 'validate'}

    @classmethod
    def _clean_kwargs(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return {k: kwargs[k] for k in kwargs if k not in cls.__OWN_ARGS}

    def __init__(self, *,
                 logger: 'Logger',
                 validate: bool,
                 output_format: OutputFormat,
                 schema_version: SchemaVersion,
                 bbc: Type['BomBuilder'],
                 **kwargs: Any) -> None:
        self._logger = logger
        self._output_format = output_format
        self._schema_version = schema_version
        self._validate = validate
        self._bbc = bbc(logger=self._logger.getChild(bbc.__name__), **self._clean_kwargs(kwargs))

    def validate(self, output: str) -> bool:
        if not self._validate:
            self._logger.warning('Validation skipped.')
            return False
        self._logger.info('Validating to schema: %s/%s', self._schema_version.to_version(), self._output_format.name)
        validation_error = make_schemabased_validator(
            self._output_format,
            self._schema_version
        ).validate_str(output)
        if validation_error:
            self._logger.debug('Validation Errors: %r', validation_error.data)
            self._logger.error('The output is invalid to schema '
                               f'{self._schema_version.to_version()}/{self._output_format.name}')
            self._logger.error('Please report the issue and provide all input data to: '
                               'https://github.com/CycloneDX/cyclonedx-python/issues/new?'
                               'template=ValidationError-report.md&labels=ValidationError&title=%5BValidationError%5D')
            raise ValueError('Output is schema-invalid')
        self._logger.info('Valid.')
        return True

    def write(self, output: str, outfile: TextIO) -> int:
        self._logger.info('Writing to: %s', outfile.name)
        written = outfile.write(output)
        self._logger.info('Wrote %i bytes to %s', written, outfile.name)
        return written

    def make_output(self, bom: 'Bom') -> str:
        self._logger.info('Serializing SBOM: %s/%s', self._schema_version.to_version(), self._output_format.name)
        return make_outputter(
            bom,
            self._output_format,
            self._schema_version
        ).output_as_string(indent=2)

    def make_bom(self, **kwargs: Any) -> 'Bom':
        self._logger.info('Generating SBOM ...')
        return self._bbc(**self._clean_kwargs(kwargs))

    def __call__(self,
                 outfile: TextIO,
                 **kwargs: Any) -> None:
        output = self.make_output(self.make_bom(**kwargs))
        self.validate(output)
        self.write(output, outfile)


def main(**kwargs: Any) -> int:
    import logging
    from sys import stderr

    arg_co = ArgumentParser(add_help=False)
    arg_co.add_argument('-v', '--verbose',
                        help='Increase the verbosity of messages (multiple for more effect) (default: silent)',
                        dest='verbosity',
                        action='count',
                        default=0)
    arg_parser = Command.make_argument_parser(sco=arg_co, **kwargs)
    del arg_co
    args = vars(arg_parser.parse_args())

    if args['command'] is None:
        arg_parser.print_help()
        return 1

    ll = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)[min(3, args.pop('verbosity'))]
    lh = logging.StreamHandler(stderr)
    lh.setLevel(ll)
    lh.setFormatter(logging.Formatter('%(levelname)-8s | %(name)s > %(message)s'))
    logger = logging.getLogger('CDX')
    logger.propagate = False
    logger.setLevel(ll)
    logger.addHandler(lh)
    del lh, ll
    logger.debug('args: %s', args)

    try:
        Command(logger=logger, **args)(**args)
    except Exception as error:
        logger.debug('Error: %s', error, exc_info=error)
        logger.critical(f'{error}')
        return 1
    return 0
