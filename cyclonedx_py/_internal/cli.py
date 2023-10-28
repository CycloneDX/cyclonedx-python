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
import argparse
import logging
from abc import ABC, abstractmethod
from sys import stderr
from typing import Any, BinaryIO, Dict, List, Optional, TextIO, Type, Union

from cyclonedx.model.bom import Bom
from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator

from .. import __version__


class CS_BomBuilder(ABC):
    @staticmethod
    @abstractmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        ...

    @abstractmethod
    def __init__(self,
                 logger: logging.Logger,
                 **kwargs: Any) -> None:
        ...

    @abstractmethod
    def __call__(self, **kwargs: Any) -> Bom:
        ...


class CS_foo(CS_BomBuilder):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_foo TODO', **kwargs)
        p.add_argument('-i', '--infile',
                       help='I HELP TODO',
                       type=argparse.FileType('rb'),
                       default='poetry.lock')
        return p

    def __init__(self,
                 logger: logging.Logger,
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self,  # type:ignore[override]
                 infile: BinaryIO,
                 **kwargs: Any) -> Bom:
        self._logger.info('ogogog')
        return Bom()


class CS_bar(CS_BomBuilder):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_bar TODO', **kwargs)
        p.add_argument('-i', '--infile',
                       help='I HELP TODO.\nSet to "-" to read from STDIN.',
                       nargs=argparse.ONE_OR_MORE,
                       type=argparse.FileType('rb'),
                       default='-')
        return p

    def __init__(self,
                 logger: logging.Logger,
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self,  # type:ignore[override]
                 infile: Union[List[BinaryIO], BinaryIO],
                 **kwargs: Any) -> Bom:
        infile = infile if isinstance(infile, list) else [infile]
        self._logger.info('lololol')
        return Bom()


class Command:
    @staticmethod
    def make_argument_parser(sco: argparse.ArgumentParser, **kwargs: Any) -> argparse.ArgumentParser:
        BooleanOptionalAction: Optional[argparse.Action] = getattr(argparse, 'BooleanOptionalAction', None)

        def mk_OutputFormatCI(value: str) -> OutputFormat:
            try:
                return OutputFormat[value.upper()]
            except KeyError:
                raise argparse.ArgumentTypeError(f'unsupported value {value!r}')

        p = argparse.ArgumentParser(
            description='description TODO',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            allow_abbrev=False,
            **kwargs)
        p.add_argument('--version', action='version', version=__version__)
        sp = p.add_subparsers(metavar='command', required=True)

        op = argparse.ArgumentParser(add_help=False)
        op.add_argument('-o', '--outfile',
                        help='O HELP TODO.\nSet to "-" to write to STDOUT.',
                        dest='outfile',
                        type=argparse.FileType('w', encoding='utf8'),
                        default='-')
        op.add_argument('--schema-version',
                        help='SV TODO\n'
                             f'{{choice: {", ".join(sorted((v.to_version() for v in SchemaVersion), reverse=True))}}}',
                        metavar='',
                        dest='schema_version',
                        choices=SchemaVersion,
                        type=SchemaVersion.from_version,
                        default=SchemaVersion.V1_4.to_version())
        op.add_argument('--output-format',
                        help='OF TODO\n'
                             f'{{choice: {", ".join(sorted(f.name for f in OutputFormat))}}}',
                        metavar='FORMAT',
                        dest='output_format',
                        choices=OutputFormat,
                        type=mk_OutputFormatCI,
                        default=OutputFormat.JSON.name)
        if BooleanOptionalAction:
            op.add_argument('--validate',
                            help='validate HELP TODO',
                            dest='validate',
                            action=argparse.BooleanOptionalAction,
                            default=True)
        else:
            vg = op.add_mutually_exclusive_group()
            vg.add_argument('--validate',
                            help='validate HELP TODO',
                            dest='validate',
                            action='store_true',
                            default=True)
            vg.add_argument('--no-validate',
                            help='no-validate HELP TODO',
                            dest='validate',
                            action='store_false')

        for sct, scc, scd in (
            ('foo', CS_foo, 'foo description'),
            ('bar', CS_bar, 'bar description'),
        ):
            spp = scc.make_argument_parser(add_help=False)
            sp.add_parser(sct,
                          help=scd,
                          description=spp.description,
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
                 logger: logging.Logger,
                 validate: bool,
                 output_format: OutputFormat,
                 schema_version: SchemaVersion,
                 bbc: Type[CS_BomBuilder],
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
            raise ValueError('output is schema-invalid to '
                             f'{self._schema_version.to_version()}/{self._output_format.name}')
        self._logger.info('Valid.')
        return True

    def write(self, output: str, outfile: TextIO) -> int:
        self._logger.info('Writing to: %s', outfile.name)
        written = outfile.write(output)
        self._logger.info('Wrote %i bytes to %s', written, outfile.name)
        return written

    def make_output(self, bom: Bom) -> str:
        self._logger.info('Serializing SBOM: %s/%s', self._schema_version.to_version(), self._output_format.name)
        return make_outputter(
            bom,
            self._output_format,
            self._schema_version
        ).output_as_string(indent=2)

    def make_bom(self, **kwargs: Any) -> Bom:
        self._logger.info('Generating SBOM ...')
        return self._bbc(**self._clean_kwargs(kwargs))

    def __call__(self,
                 outfile: TextIO,
                 **kwargs: Any) -> None:
        output = self.make_output(self.make_bom(**kwargs))
        self.validate(output)
        self.write(output, outfile)


def main(**kwargs: Any) -> int:
    arg_co = argparse.ArgumentParser(add_help=False)
    arg_co.add_argument('-v', '--verbose',
                        help='verbose help TODO',
                        dest='verbosity',
                        action='count',
                        default=0)
    arg_parser = Command.make_argument_parser(sco=arg_co, **kwargs)
    del arg_co
    args = vars(arg_parser.parse_args())

    ll = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)[min(3, args.pop('verbosity'))]
    lh = logging.StreamHandler(stderr)
    lh.setLevel(ll)
    lh.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(ll)
    logger.addHandler(lh)
    del lh, ll
    logger.debug('args: %s', args)

    try:
        Command(logger=logger, **args)(**args)
    except Exception as error:
        logger.exception('Error: %s', error, exc_info=error)
        return 1
    return 0
