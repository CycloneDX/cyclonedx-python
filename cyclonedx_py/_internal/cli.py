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
from abc import ABC, abstractmethod
from sys import stderr, stdin, stdout
from typing import Any, Optional, Type

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

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args

    @abstractmethod
    def __call__(self) -> Bom:
        ...


class CS_foo(CS_BomBuilder):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_foo TODO', **kwargs)
        p.add_argument('-i', '--infile', help='I HELP TODO',
                       type=argparse.FileType('rb'), default='poetry.lock')
        return p

    def __call__(self) -> Bom:
        # print(self._args, file=stderr)
        return Bom()


class CS_bar(CS_BomBuilder):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_bar TODO', **kwargs)
        p.add_argument('-i', '--infile', help='I HELP TODO', nargs=argparse.ONE_OR_MORE,
                       type=argparse.FileType('rb'), default=[stdin.buffer])
        return p

    def __call__(self) -> Bom:
        # print(self._args, file=stderr)
        return Bom()


class Command:
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        BooleanOptionalAction: Optional[argparse.Action] = getattr(argparse, 'BooleanOptionalAction', None)

        p = argparse.ArgumentParser(
            description='description TODO',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            **kwargs)
        p.add_argument('--version', action='version', version=__version__)
        sp = p.add_subparsers(metavar='command', required=True)

        op = argparse.ArgumentParser(add_help=False, formatter_class=p.formatter_class)
        op.add_argument('-o', '--outfile',
                        help='O HELP TODO',
                        dest='outfile',
                        type=argparse.FileType('w', encoding='utf8'),
                        default='-')
        op.add_argument('--schema-version',
                        dest='schemaVersion',
                        metavar='SCHEMA_VERSION',
                        choices=sorted((v.to_version() for v in SchemaVersion), reverse=True),
                        type=SchemaVersion.from_version,
                        default=SchemaVersion.V1_4.to_version())
        op.add_argument('--output-format',
                        dest='outputFormat',
                        metavar='OUTPUT_FORMAT',
                        choices=sorted(f.name for f in OutputFormat),
                        type=lambda v: OutputFormat[v.upper()],
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
            del vg

        sct: str
        scc: Type[CS_BomBuilder]
        scd: str
        for sct, scc, scd in (
            ('foo', CS_foo, 'foo description'),
            ('bar', CS_bar, 'bar description'),
        ):
            spp = scc.make_argument_parser(add_help=False, formatter_class=p.formatter_class)
            sp.add_parser(sct,
                          help=scd,
                          description=spp.description,
                          parents=[spp, op],
                          formatter_class=p.formatter_class
                          ).set_defaults(bbc=scc)
            del sct, scc, scd

        return p

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args

    def __call__(self) -> int:
        print('generating bom...', file=stderr)
        try:
            bom = self._args.bbc(self._args)()
        except Exception as error:
            print('Unexpected Error:', error, file=stderr)
            return 1
        print('generating bom result...', file=stderr)
        try:
            outputter = make_outputter(bom, self._args.outputFormat, self._args.schemaVersion)
            output = outputter.output_as_string(indent=2)
        except Exception as error:
            print('Output Errors:', error, file=stderr)
            return 1
        if self._args.validate:
            print('validating bom result...', file=stderr)
            validation_error = make_schemabased_validator(
                outputter.output_format,
                outputter.schema_version
            ).validate_str(output)
            if validation_error is not None:
                print('Validation Errors:', validation_error.data, file=stderr)
                return 2
            print('bom result valid.', file=stderr)
        else:
            print('skipped validation.', file=stderr)
        print('writing to', self._args.outfile.name, file=stderr)
        written = self._args.outfile.write(output)
        self._args.outfile.close()
        # start with a line break, to finalize possibly unterminated output.
        print('\nwrote', written, 'bytes to', self._args.outfile.name, file=stderr)
        return 0


def main(**kwargs: Any) -> int:
    return Command(Command.make_argument_parser(**kwargs).parse_args())()