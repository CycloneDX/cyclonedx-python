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
from json import dumps as json_dumps
from os import getenv
from os.path import dirname, join
from typing import Union
from unittest import TestCase

from cyclonedx.schema import OutputFormat

from cyclonedx_py import __version__ as thisVersion

_TESTDATA_DIRECTORY = join(dirname(__file__), '_data')

INFILES_DIRECTORY = join(_TESTDATA_DIRECTORY, 'infiles')
SNAPSHOTS_DIRECTORY = join(_TESTDATA_DIRECTORY, 'snapshots')

RECREATE_SNAPSHOTS = '1' == getenv('CDX_TEST_RECREATE_SNAPSHOTS')
if RECREATE_SNAPSHOTS:
    print('!!! WILL RECREATE ALL SNAPSHOTS !!!')


class SnapshotMixin:

    @staticmethod
    def getSnapshotFile(snapshot_name: str) -> str:  # noqa: N802
        return join(SNAPSHOTS_DIRECTORY, f'{snapshot_name}.bin')

    @classmethod
    def writeSnapshot(cls, snapshot_name: str, data: str) -> None:  # noqa: N802
        with open(cls.getSnapshotFile(snapshot_name), 'w') as s:
            s.write(data)

    @classmethod
    def readSnapshot(cls, snapshot_name: str) -> str:  # noqa: N802
        with open(cls.getSnapshotFile(snapshot_name), 'r') as s:
            return s.read()

    def assertEqualSnapshot(self: Union[TestCase, 'SnapshotMixin'],  # noqa: N802
                            actual: str, snapshot_name: str) -> None:
        if RECREATE_SNAPSHOTS:
            self.writeSnapshot(snapshot_name, actual)
        _omd = self.maxDiff
        _omd = self.maxDiff
        self.maxDiff = None
        try:
            self.assertEqual(actual, self.readSnapshot(snapshot_name))
        finally:
            self.maxDiff = _omd


# region reproducible test results

def make_xml_comparable(bom: str) -> str:
    bom = re.sub(' serialNumber=".+?"', '', bom)
    bom = re.sub(r'\s*<timestamp>.*?</timestamp>', '', bom)
    bom = bom.replace(  # replace metadata.tools.version
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-bom</name>\n'
        f'        <version>{thisVersion}</version>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-bom</name>\n'
        '        <version>thisVersion-testing</version>')
    bom = re.sub(  # replace metadata.tools.version
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>.*?</version>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>libVersion-testing</version>',
        bom)
    return bom


def make_json_comparable(bom: str) -> str:
    bom = re.sub(r'\s*"(?:timestamp|serialNumber)": ".+?",?', '', bom)
    bom = bom.replace(  # replace metadata.tools.version
        '        "name": "cyclonedx-bom",\n'
        '        "vendor": "CycloneDX",\n'
        f'        "version": {json_dumps(thisVersion)}',
        '        "name": "cyclonedx-bom",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "thisVersion-testing"')
    bom = re.sub(  # replace metadata.tools.version
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": ".*?"',
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "libVersion-testing"',
        bom)
    return bom


def make_comparable(bom: str, of: OutputFormat) -> str:
    if of is OutputFormat.XML:
        return make_xml_comparable(bom)
    if of is OutputFormat.JSON:
        return make_json_comparable(bom)
    raise NotImplementedError(f'unknown OutputFormat: {of!r}')

# endregion reproducible test results