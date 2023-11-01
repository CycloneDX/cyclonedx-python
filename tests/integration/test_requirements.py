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


import re
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import StringIO
from os.path import basename, join
from typing import Union
from unittest import TestCase
from unittest.mock import patch

from cyclonedx.model.bom import Bom
from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from cyclonedx_py._internal.cli import main
from tests import INFILES_DIRECTORY, SnapshotMixin

infiles = glob(join(INFILES_DIRECTORY, 'requirements', '*'))
unsupported_of_sf = [
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
]


def make_bank_bom() -> Bom:
    bom = Bom()
    bom.serial_number = None
    bom.metadata.tools.clear()
    bom.metadata.timestamp = None
    return bom


@ddt
class TestRequirements(TestCase, SnapshotMixin):

    @named_data(*(
        [f'{basename(infile)}-{sv.name}-{of.name}', infile, sv, of]
        for infile in infiles
        for sv in SchemaVersion
        for of in OutputFormat
        if (of, sv) not in unsupported_of_sf
    ))
    @patch('cyclonedx_py._internal.utils.bom.make_bom', make_bank_bom)
    def test_cli_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with StringIO() as err, StringIO() as out:
            err.name = 'fakeerr'
            out.name = 'fakeout'
            with redirect_stderr(err), redirect_stdout(out):
                res = main(argv=[
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
            out,
            f'{basename(infile)}-{sv.to_version()}.{of.name.lower()}')

    def assertEqualSnapshot(self, actual: str, snapshot_name: str) -> None:
        super().assertEqualSnapshot(actual, join('requirements', snapshot_name))
