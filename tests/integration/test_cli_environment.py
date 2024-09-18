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

import random
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO
from os import name as os_name
from os.path import basename, dirname, join
from subprocess import run  # nosec:B404
from sys import executable, stderr
from typing import Any, Generator
from unittest import TestCase, skipIf

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import run as run_cli
from tests import INFILES_DIRECTORY, INIT_TESTBEDS, SUPPORTED_OF_SV, SnapshotMixin, make_comparable

initfiles = glob(join(INFILES_DIRECTORY, 'environment', '*', 'init.py'))
test_data = tuple(
    (f'{basename(projectdir)}-{sv.name}-{of.name}', projectdir, sv, of)
    for projectdir in map(dirname, initfiles)
    for of, sv in SUPPORTED_OF_SV
)


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


@ddt
class TestCliEnvironment(TestCase, SnapshotMixin):

    @classmethod
    def __setup_testbeds_init(cls) -> None:
        for initfile in initfiles:
            print('setup init testbed:', initfile, file=stderr)
            res = run((executable, initfile),
                      capture_output=True, encoding='utf8', errors='replace', shell=False)  # nosec:B603
            if res.returncode != 0:
                raise RuntimeError(
                    f'failed init: {initfile}\nstdout: {res.stdout}\nstderr: {res.stderr}\n')

    @classmethod
    def setUpClass(cls) -> None:
        if INIT_TESTBEDS:
            cls.__setup_testbeds_init()

    @named_data(
        ('does-not-exist', 'something-that-must-not-exist.testing', 'No such file or directory'),
        ('no-env', join(INFILES_DIRECTORY, 'environment', 'broken-env'), 'Failed to find python in directory'),
    )
    def test_fails_with_python_not_found(self, wrong_python: str, expected_error: str) -> None:
        _, _, sv, of = random.choice(test_data)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    wrong_python])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn(expected_error, err)

    @named_data(
        ('exit-non-zero', join(INFILES_DIRECTORY, 'environment', 'broken-env', 'non-zero.py'), 'Fail fetching `path`'),
        ('no-json', join(INFILES_DIRECTORY, 'environment', 'broken-env', 'broken-json.py'), 'JSONDecodeError'),
    )
    @skipIf(os_name == 'nt', 'cannot run on win')
    def test_fails_with_python_unexpected(self, wrong_python: str, expected_error: str) -> None:
        _, _, sv, of = random.choice(test_data)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    f'--sv={sv.to_version()}',
                    f'--of={of.name}',
                    '--outfile=-',
                    wrong_python])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn(expected_error, err)

    def test_with_pyproject_not_found(self) -> None:
        _, projectdir, sv, of = random.choice(test_data)  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--outfile=-',
                    '--pyproject=something-that-must-not-exist.testing',
                    projectdir
                ])
            err = err.getvalue()
            out = out.getvalue()
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open pyproject file: something-that-must-not-exist.testing', err)

    def test_with_current_python(self) -> None:
        sv = SchemaVersion.V1_6
        of = random.choice((OutputFormat.XML, OutputFormat.JSON))  # nosec B311
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    # no project dir -> search in current python
                ])
                err = err.getvalue()
                sbom1 = out.getvalue()
        self.assertEqual(0, res, err)
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    executable  # explicitly current python
                ])
            err = err.getvalue()
            sbom2 = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqual(
            make_comparable(sbom1, of),
            make_comparable(sbom2, of)
        )

    @named_data(*test_data)
    def test_plain_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', join(projectdir, 'pyproject.toml'),
                    join(projectdir, '.venv')])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'plain', projectdir, sv, of)

    @named_data(*test_data_file_filter('pep639'))
    def test_pep639_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', join(projectdir, 'pyproject.toml'),
                    '--PEP-639',
                    join(projectdir, '.venv')])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'pep639', projectdir, sv, of)

    @named_data(*test_data_file_filter('pep639'))
    def test_pep639_texts_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', join(projectdir, 'pyproject.toml'),
                    '--PEP-639',
                    '--gather-license-texts',
                    join(projectdir, '.venv')])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'pep639-texts', projectdir, sv, of)

    @named_data(*test_data_file_filter('pep639'))
    def test_texts_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = '<fakeerr>'
            out.name = '<fakeout>'
            with redirect_stderr(err), redirect_stdout(out):
                res = run_cli(argv=[
                    'environment',
                    '-vvv',
                    '--sv', sv.to_version(),
                    '--of', of.name,
                    '--output-reproducible',
                    '--outfile=-',
                    '--pyproject', join(projectdir, 'pyproject.toml'),
                    '--gather-license-texts',
                    join(projectdir, '.venv')])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'texts', projectdir, sv, of)

    def assertEqualSnapshot(  # noqa:N802
        self, actual: str,
        purpose: str,
        projectdir: str,
        sv: SchemaVersion,
        of: OutputFormat
    ) -> None:
        super().assertEqualSnapshot(
            make_comparable(actual, of),
            join('environment', f'{purpose}_{basename(projectdir)}_{sv.to_version()}.{of.name.lower()}')
        )
