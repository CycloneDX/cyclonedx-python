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


import random
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO
from os.path import basename, dirname, join
from typing import Any, Generator
from unittest import TestCase

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import run as run_cli
from tests import INFILES_DIRECTORY, SnapshotMixin, make_comparable

lockfiles = glob(join(INFILES_DIRECTORY, 'poetry', '*', '*', 'poetry.lock'))
projectdirs = list(dirname(lockfile) for lockfile in lockfiles)

unsupported_of_sf = [
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
]

test_data = [
    (f'{basename(dirname(projectdir))}-{basename(projectdir)}-{sv.name}-{of.name}', projectdir, sv, of)
    for projectdir in projectdirs
    for sv in SchemaVersion
    for of in OutputFormat
    if (of, sv) not in unsupported_of_sf
]


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


@ddt
class TestPoetry(TestCase, SnapshotMixin):

    def test_cli_fails_with_dir_not_found(self) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    f'--sv={SchemaVersion.V1_4.to_version()}',
                    f'--of={OutputFormat.XML.name}',
                    '--outfile=-',
                    'something-that-must-not-exist.testing'])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn("No such file or directory: 'something-that-must-not-exist.testing", err)

    def test_cli_fails_with_groups_not_found(self) -> None:
        projectdir = random.choice(projectdirs)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    '--with', 'MNE-with-A',
                    '--with', 'MNE-with-B,MNE-with-C',
                    '--without', 'MNE-without-A',
                    '--without', 'MNE-without-B,MNE-without-C',
                    '--only', 'MNE-only-A',
                    '--only', 'MNE-only-B,MNE-only-C',
                    projectdir])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn('Group(s) not found:'
                      " 'MNE-only-A' (via only),"
                      " 'MNE-only-B' (via only),"
                      " 'MNE-only-C' (via only),"
                      " 'MNE-with-A' (via with),"
                      " 'MNE-with-B' (via with),"
                      " 'MNE-with-C' (via with),"
                      " 'MNE-without-A' (via without),"
                      " 'MNE-without-B' (via without),"
                      " 'MNE-without-C' (via without)", err)

    def test_cli_fails_with_extras_not_found(self) -> None:
        projectdir = random.choice(projectdirs)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    '-E', 'MNE-extra-C,MNE-extra-B',
                    '--extras', 'MNE-extra-A',
                    projectdir])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn('Extra(s) ['
                      'MNE-extra-A,'
                      'MNE-extra-B,'
                      'MNE-extra-C'
                      '] not specified', err)

    @named_data(*test_data)
    def test_cli_with_file_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    projectdir])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(
            make_comparable(out, of),
            f'{basename(dirname(projectdir))}-{basename(projectdir)}-{sv.to_version()}.{of.name.lower()}')

    @named_data(*test_data_file_filter('group-deps'))
    def test_cli_with_groups_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    '--with', 'groupA',
                    '--without', 'groupB,dev',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    projectdir])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(
            make_comparable(out, of),
            f'some-groups-{basename(projectdir)}-{sv.to_version()}.{of.name.lower()}')

    @named_data(*test_data_file_filter('with-extras'))
    def test_cli_with_extras_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'poetry',
                    '-vvv',
                    '-E', 'my-extra',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    projectdir])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(
            make_comparable(out, of),
            f'some-extras-{basename(projectdir)}-{sv.to_version()}.{of.name.lower()}')

    def assertEqualSnapshot(self, actual: str, snapshot_name: str) -> None:  # noqa:N802
        super().assertEqualSnapshot(actual, join('poetry', snapshot_name))
