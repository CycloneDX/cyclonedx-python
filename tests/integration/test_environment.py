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


from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO
from os.path import basename, dirname, join
from subprocess import run  # nosec:B404
from sys import executable
from typing import Any, Generator
from unittest import TestCase

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import run as run_cli
from tests import INFILES_DIRECTORY, SUPPORTED_OF_SV, SnapshotMixin, make_comparable

initfiles = glob(join(INFILES_DIRECTORY, 'environment', '*', 'init.py'))
projectdirs = list(dirname(initfile) for initfile in initfiles)

test_data = tuple(
    (f'{basename(projectdir)}-{sv.name}-{of.name}', projectdir, sv, of)
    for projectdir in projectdirs
    for of, sv in SUPPORTED_OF_SV
)


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


@ddt
class TestPipenv(TestCase, SnapshotMixin):

    @classmethod
    def setUpClass(cls) -> None:
        for initfile in initfiles:
            res = run([executable, initfile],
                      capture_output=True, encoding='utf8', shell=False)   # nosec:B603
            if res.returncode != 0:
                raise RuntimeError(f'failed init :\n'
                                   f'stdout: {res.stdout}\n'
                                   f'stderr: {res.stderr}\n')

    def test_cli_fails_with_python_not_found(self) -> None:
        pass  # TODO fails

    def test_cli_with_current_python(self) -> None:
        pass  # TODO does not fail

    @named_data(*test_data)
    def test_cli_with_file_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
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
                    f'--pyproject={join(projectdir, "pyproject.toml")}',
                    join(projectdir, '.venv')])
            err = err.getvalue()
            out = out.getvalue()
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'venv', projectdir, sv, of)

    def assertEqualSnapshot(self, actual: str,  # noqa:N802
                            purpose: str,
                            projectdir: str,
                            sv: SchemaVersion,
                            of: OutputFormat
                            ) -> None:
        super().assertEqualSnapshot(
            make_comparable(actual, of),
            join('environment', f'{purpose}_{basename(projectdir)}_{sv.to_version()}.{of.name.lower()}')
        )
