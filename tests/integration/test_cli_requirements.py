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


import os
import random
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO, TextIOWrapper
from os.path import basename, join, splitext
from typing import Any, Generator, Tuple
from unittest import TestCase
from unittest.mock import patch

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import run as run_cli
from tests import INFILES_DIRECTORY, SUPPORTED_OF_SV, SnapshotMixin, make_comparable

infiles = glob(join(INFILES_DIRECTORY, 'requirements', '*.txt*'))

pyproject_file = join(INFILES_DIRECTORY, 'requirements', 'pyproject.toml')

test_data = tuple(
    (f'{splitext(basename(infile))[0]}-{sv.name}-{of.name}', infile, sv, of)
    for infile in infiles
    for of, sv in SUPPORTED_OF_SV
)


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


if os.name == 'nt':
    def test_data_os_filter(data: Any) -> bool:
        return True
else:
    def test_data_os_filter(data: Tuple[Any, str, Any, Any]) -> bool:
        # skip windows encoded files on non-windows
        return '.cp125' not in data[1]


@ddt
class TestCliRequirements(TestCase, SnapshotMixin):

    def test_with_file_not_found(self) -> None:
        _, infile, sv, of = random.choice(test_data)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--outfile=-',
                    'something-that-must-not-exist.testing'])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open requirements file: something-that-must-not-exist.testing', err)

    def test_with_pyproject_not_found(self) -> None:
        _, infile, sv, of = random.choice(test_data)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--outfile=-',
                    '--pyproject=something-that-must-not-exist.testing',
                    infile
                ])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open pyproject file: something-that-must-not-exist.testing', err)

    @named_data(*filter(test_data_os_filter, test_data))
    def test_with_file_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', pyproject_file,
                    infile])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'file', infile, sv, of)

    @named_data(*test_data)
    def test_with_stream_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out, open(infile, 'rb') as inp:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                with patch('sys.stdin', TextIOWrapper(inp)):
                    res = run_cli(argv=[
                        'requirements',
                        '-vvv',
                        '--sv', sv.to_version(),
                        '--of', of.name,
                        '--output-reproducible',
                        '--outfile=-',
                        # no pyproject for this case
                        '-'])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'stream', infile, sv, of)

    @named_data(*test_data_file_filter('frozen'))
    def test_with_index_auth(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    '--index-url', 'https://user:password@pypackages.acme.org/simple/',
                    '--extra-index-url', 'https://user:password@legacy1.pypackages.acme.org/simple/',
                    '--extra-index-url', 'https://user:password@legacy2.pypackages.acme.org/simple/',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', pyproject_file,
                    infile])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'index_auth', infile, sv, of)

    def assertEqualSnapshot(self, actual: str,  # noqa:N802
                            purpose: str,
                            reqfile: str,
                            sv: SchemaVersion,
                            of: OutputFormat
                            ) -> None:
        super().assertEqualSnapshot(
            make_comparable(actual, of),
            join('requirements', f'{purpose}_{splitext(basename(reqfile))[0]}_{sv.to_version()}.{of.name.lower()}')
        )
