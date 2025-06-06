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

import logging
import sys
from argparse import ArgumentParser, BooleanOptionalAction, FileType, RawDescriptionHelpFormatter
from collections.abc import Sequence
from itertools import chain
from typing import TYPE_CHECKING, Any, NoReturn, Optional, TextIO, Union

from cyclonedx.model import Property
from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator

from .. import __version__
from . import PropertyName, PropertyValue
from .environment import EnvironmentBB
from .pipenv import PipenvBB
from .poetry import PoetryBB
from .requirements import RequirementsBB
from .utils.args import argparse_type4enum, choices4enum

if TYPE_CHECKING:  # pragma: no cover
    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component

    from . import BomBuilder

OPTION_OUTPUT_STDOUT = '-'


class Command:
    @classmethod
    def make_argument_parser(cls, sco: ArgumentParser, **kwargs: Any) -> ArgumentParser:
        # region Command
        p = ArgumentParser(
            description='Creates CycloneDX Software Bill of Materials (SBOM) from Python projects and environments.',
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
            **kwargs)
        p.add_argument('--version', action='version', version=__version__)
        sp = p.add_subparsers(metavar='<command>', dest='command',
                              # not required. if omitted: show help and exit
                              required=False)
        # region Command

        # region SubCOmmand
        op = ArgumentParser(add_help=False)
        op.add_argument('--short-PURLs',
                        help='Omit all qualifiers from PackageURLs.\n'
                             'This causes information loss in trade-off shorter PURLs, '
                             'which might improve ingesting these strings.',
                        action='store_true',
                        dest='short_purls',
                        default=False)
        op.add_argument('--sv', '--spec-version',
                        metavar='<version>',
                        help='Which version of CycloneDX to use.'
                        f' {{choices: {", ".join(sorted((v.to_version() for v in SchemaVersion), reverse=True))}}}'
                        ' (default: %(default)s)',
                        dest='spec_version',
                        choices=SchemaVersion,
                        type=SchemaVersion.from_version,
                        default=SchemaVersion.V1_6.to_version())
        op.add_argument('--output-reproducible',
                        help='Whether to go the extra mile and make the output reproducible.\n'
                        'This might result in loss of time- and random-based values.',
                        action='store_true',
                        dest='output_reproducible',
                        default=False)
        op.add_argument('--of', '--output-format',
                        metavar='<format>',
                        help='Which output format to use.'
                        f' {choices4enum(OutputFormat)}'
                        ' (default: %(default)s)',
                        dest='output_format',
                        choices=OutputFormat,
                        type=argparse_type4enum(OutputFormat),
                        default=OutputFormat.JSON.name)
        op.add_argument('-o', '--output-file',
                        metavar='<file>',
                        help='Path to the output file.'
                        f' (set to "{OPTION_OUTPUT_STDOUT}" to output to <stdout>)'
                        ' (default: %(default)s)',
                        type=FileType('wt', encoding='utf8'),
                        dest='output_file',
                        default=OPTION_OUTPUT_STDOUT)
        op.add_argument('--validate',
                        help='Whether to validate resulting BOM before outputting.'
                             ' (default: %(default)s)',
                        action=BooleanOptionalAction,
                        dest='should_validate',
                        default=True)

        scbbc: type['BomBuilder']
        sct: str
        scta: list[str]
        for scbbc, sct, *scta in (
            (EnvironmentBB, 'environment', 'env', 'venv'),
            (RequirementsBB, 'requirements'),
            (PipenvBB, 'pipenv'),
            (PoetryBB, 'poetry'),
        ):
            spp = scbbc.make_argument_parser(add_help=False)
            sp.add_parser(sct, aliases=scta,
                          help=(spp.description or '').split('\n')[0].strip('. '),
                          description=spp.description,
                          epilog=spp.epilog,
                          parents=[spp, op, sco],
                          formatter_class=p.formatter_class,
                          allow_abbrev=p.allow_abbrev,
                          ).set_defaults(_bbc=scbbc)
        # endregion SubCommand

        return p

    __OWN_ARGS = {
        # the arg keywords from __init__()
        'logger', 'short_purls', 'output_format', 'spec_version', 'output_reproducible', 'should_validate',
        # the arg keywords from __call__()
        'output_file'
    }

    @classmethod
    def _clean_kwargs(cls, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {k: kwargs[k] for k in kwargs if k not in cls.__OWN_ARGS}

    def __init__(self, *,
                 logger: logging.Logger,
                 short_purls: bool,
                 output_format: OutputFormat,
                 spec_version: SchemaVersion,
                 output_reproducible: bool,
                 should_validate: bool,
                 _bbc: type['BomBuilder'],
                 **kwargs: Any) -> None:
        self._logger = logger
        self._short_purls = short_purls
        self._output_format = output_format
        self._spec_version = spec_version
        self._output_reproducible = output_reproducible
        self._should_validate = should_validate
        self._bbc = _bbc(**self._clean_kwargs(kwargs),
                         logger=self._logger.getChild(_bbc.__name__))

    def _shorten_purls(self, bom: 'Bom') -> bool:
        if not self._short_purls:
            return False

        self._logger.info('Shorting purls...')
        component: 'Component'
        for component in chain(
            bom.metadata.component.get_all_nested_components(True) if bom.metadata.component else (),
            chain.from_iterable(
                component.get_all_nested_components(True) for component in bom.components
            )
        ):
            if component.purl is not None:
                purl = component.purl
                component.purl = type(purl)(
                    type=purl.type,
                    namespace=purl.namespace,
                    name=purl.name,
                    version=purl.version
                    # omit qualifiers
                    # omit subdirectory
                )
        return True

    def _validate(self, output: str) -> bool:
        if not self._should_validate:
            self._logger.warning('Validation skipped.')
            return False

        self._logger.info('Validating result to spec: %s/%s',
                          self._spec_version.to_version(), self._output_format.name)

        validation_error = make_schemabased_validator(
            self._output_format,
            self._spec_version
        ).validate_str(output)
        if validation_error:
            self._logger.debug('Validation Errors: %r', validation_error.data)
            self._logger.error('The result is invalid to schema '
                               f'{self._spec_version.to_version()}/{self._output_format.name}')
            self._logger.warning('Please report the issue and provide all input data to: '
                                 'https://github.com/CycloneDX/cyclonedx-python/issues/new?'
                                 'template=ValidationError-report.md&'
                                 'labels=ValidationError&title=%5BValidationError%5D')
            raise ValueError('result is schema-invalid')
        self._logger.debug('result is schema-valid')
        return True

    def _write(self, output: str, output_file: TextIO) -> int:
        self._logger.info('Writing to: %s', output_file.name)
        written = output_file.write(output)
        self._logger.debug('Wrote %i bytes to %s', written, output_file.name)
        return written

    def _make_output(self, bom: 'Bom') -> str:
        self._logger.info('Serializing SBOM: %s/%s', self._spec_version.to_version(), self._output_format.name)

        if self._output_reproducible:
            bom.metadata.properties.add(Property(name=PropertyName.Reproducible.value,
                                                 value=PropertyValue.BooleanTrue.value))
            # dirty hacks to remove these mandatory properties
            bom.serial_number = None  # type:ignore[assignment]
            bom.metadata.timestamp = None  # type:ignore[assignment]

        return make_outputter(
            bom,
            self._output_format,
            self._spec_version
        ).output_as_string(indent=2)

    def _make_bom(self, **kwargs: Any) -> 'Bom':
        self._logger.info('Generating SBOM ...')
        return self._bbc(**self._clean_kwargs(kwargs))

    def __call__(self,
                 output_file: TextIO,
                 **kwargs: Any) -> None:
        bom = self._make_bom(**kwargs)
        self._shorten_purls(bom)
        output = self._make_output(bom)
        del bom
        self._validate(output)
        self._write(output, output_file)


def run(*, argv: Optional[Sequence[str]] = None, **kwargs: Any) -> Union[int, NoReturn]:
    arg_co = ArgumentParser(add_help=False)
    arg_co.add_argument('-v', '--verbose',
                        help='Increase the verbosity of messages'
                             ' (multiple for more effect)'
                             ' (default: silent)',
                        dest='verbosity',
                        action='count',
                        default=0)
    arg_parser = Command.make_argument_parser(**kwargs, sco=arg_co)
    del arg_co, kwargs
    args = vars(arg_parser.parse_args(argv))  # may exit -> raise `SystemExit`
    if args['command'] is None:
        # print the "help" page on error, instead of printing "usage" page
        # this is done to have a better user experience.
        arg_parser.print_help()
        sys.exit(1)
    del arg_parser, argv

    ll = (logging.WARNING, logging.INFO, logging.DEBUG)[min(2, args.pop('verbosity'))]
    lh = logging.StreamHandler(sys.stderr)
    lh.setLevel(ll)
    lh.setFormatter(logging.Formatter('%(levelname)-8s | %(name)s > %(message)s'))
    logger = logging.getLogger('CDX')
    logger.propagate = False
    logger.setLevel(lh.level)
    logger.addHandler(lh)

    logger.debug('args: %s', args)
    try:
        Command(**args, logger=logger)(**args)
    except Exception as error:
        logger.debug('Error: %s', error, exc_info=error)
        logger.critical(f'{error}')
        return 1
    else:
        return 0
    finally:
        # if called programmatically (in tests), the handlers would stack up,
        # since the logger is registered globally static
        logger.removeHandler(lh)
