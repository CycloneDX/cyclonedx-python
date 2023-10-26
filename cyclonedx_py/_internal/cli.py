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
from sys import stdin, stdout, stderr
from abc import ABC, abstractmethod
from typing import Any, Optional, Type
from .. import __version__


class CS_Proto(ABC):
    @staticmethod
    @abstractmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        ...

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args

    @abstractmethod
    def __call__(self) -> int:
        ...


class CS_foo(CS_Proto):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_foo TODO', **kwargs)
        p.add_argument('-i', '--infile', help='I HELP TODO', nargs='+', type=argparse.FileType('rb'), default='poetry.lock')
        return p

    def __call__(self) -> int:
        print(self._args, file=stderr)
        return 0


class CS_bar(CS_Proto):
    @staticmethod
    def make_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description='description CS_bar TODO', **kwargs)
        p.add_argument('-i', '--infile', help='I HELP TODO', nargs='?', type=argparse.FileType('rb'), default='-')
        return p

    def __call__(self) -> int:
        print(self._args, file=stderr)
        return 0


def make_cli(**kwargs: Any) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description='description TODO',
        **kwargs)
    p.add_argument('--version', action='version', version=__version__)
    sp = p.add_subparsers(metavar='command', required=True)

    op = argparse.ArgumentParser(add_help=False)
    opg = op.add_argument_group(title='OPG TODO')
    opg.add_argument('-o', '--outfile', help='O HELP TODO', nargs='?', type=argparse.FileType('w', encoding='utf8'), default='-')
    BooleanOptionalAction: Optional[argparse.Action] = getattr(argparse, 'BooleanOptionalAction', None)
    if BooleanOptionalAction:
        opg.add_argument('--validate', help='validate HELP TODO', action=argparse.BooleanOptionalAction, default=True)
    else:
        vg = opg.add_mutually_exclusive_group()
        vg.add_argument('--validate', help='validate HELP TODO', action='store_true', default=True)
        vg.add_argument('--no-validate', help='no-validate HELP TODO', action='store_false')
        del vg

    sct: str
    scc: Type[CS_Proto]
    scd: str
    for sct, scc, scd in (
        ('foo', CS_foo, 'foo description'),
        ('bar', CS_bar, 'bar description'),
    ):
        spp = scc.make_argument_parser(add_help=False)
        sp.add_parser(sct,
                      help=scd,
                      description=spp.description,
                      parents=[spp, opg]
                      ).set_defaults(scc=scc)
        del spp

    return p


def main(**kwargs: Any) -> int:
    args = make_cli(**kwargs).parse_args()
    return args.scc(args)()
