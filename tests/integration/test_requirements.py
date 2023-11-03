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


import os
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO, TextIOWrapper
from os.path import basename, join
from typing import Any, Tuple
from unittest import TestCase
from unittest.mock import patch

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import run as run_cli
from tests import INFILES_DIRECTORY, SnapshotMixin, make_comparable

infiles = glob(join(INFILES_DIRECTORY, 'requirements', '*'))
unsupported_of_sf = [
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
]

test_data = [
    (f'{basename(infile)}-{sv.name}-{of.name}', infile, sv, of)
    for infile in infiles
    for sv in SchemaVersion
    for of in OutputFormat
    if (of, sv) not in unsupported_of_sf
]

if os.name == 'nt':
    def test_data_os_filter(data: Any) -> bool:
        return True
else:
    def test_data_os_filter(data: Tuple[Any, str, Any, Any]) -> bool:
        # skip windows encoded files on non-windows
        return '.cp125' not in data[1]


@ddt
class TestRequirements(TestCase, SnapshotMixin):

    def test_cli_with_file_not_found(self) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    f'--sv={SchemaVersion.V1_4.to_version()}',
                    f'--of={OutputFormat.XML.name}',
                    '--outfile=-',
                    'something-that-must-not-exist.testing'])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn("No such file or directory: 'something-that-must-not-exist.testing'", err)

    @named_data(*filter(test_data_os_filter, test_data))
    def test_cli_with_file_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'requirements',
                    '-vvv',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    infile])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(
            make_comparable(out, of),
            f'{basename(infile)}-{sv.to_version()}.{of.name.lower()}-file')

    @named_data(*test_data)
    def test_cli_with_stream_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out, open(infile, 'rb') as inp:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                with patch('sys.stdin', TextIOWrapper(inp)):
                    res = run_cli(argv=[
                        'requirements',
                        '-vvv',
                        f'--sv={sv.to_version()}',
                        f'--of={of.name}',
                        '--outfile=-',
                        '-'])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(
            make_comparable(out, of),
            f'{basename(infile)}-{sv.to_version()}.{of.name.lower()}-stream')

    def assertEqualSnapshot(self, actual: str, snapshot_name: str) -> None:
        super().assertEqualSnapshot(actual, join('requirements', snapshot_name))
