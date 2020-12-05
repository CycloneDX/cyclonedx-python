# This file is part of CycloneDX Python module.
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
# Copyright (c) Steve Springett. All Rights Reserved.

import os.path
import subprocess
import tempfile
import pytest
from cyclonedx.client import build_parser, generate_bom


script_path = os.path.dirname(__file__)


def test_xml_bom_generation():
    with tempfile.TemporaryDirectory() as dirname:
        # arrange
        with open(os.path.join(script_path, 'resources', 'bom.xml'), 'r') as bf:
            expected_xml = bf.read()
        
        # act
        subprocess.check_output([
            'cyclonedx-py',
            '-i', os.path.join(script_path, 'resources', 'requirements.txt'),
            '-o', os.path.join(dirname, 'bom.xml'),
        ])

        # assert
        with open(os.path.join(dirname, 'bom.xml'), 'rt') as f:
            actual_xml = f.read()
        assert actual_xml == expected_xml


def test_json_bom_generation():
    with tempfile.TemporaryDirectory() as dirname:
        # arrange
        with open(os.path.join(script_path, 'resources', 'bom.json'), 'r') as bf:
            expected_json = bf.read()
        
        # act
        subprocess.check_output([
            'cyclonedx-py',
            '-i', os.path.join(script_path, 'resources', 'requirements.txt'),
            '-o', os.path.join(dirname, 'bom.json'),
            '-j',
        ])

        # assert
        with open(os.path.join(dirname, 'bom.json'), 'rt') as f:
            actual_json = f.read()
        assert actual_json == expected_json

def test_invalid_xml_characters():
    with tempfile.TemporaryDirectory() as dirname:
        # arrange
        with open(os.path.join(script_path, 'resources', 'invalid-xml-characters', 'bom.xml'), 'r') as bf:
            expected_xml = bf.read()
        
        # act
        subprocess.check_output([
            'cyclonedx-py',
            '-i', os.path.join(script_path, 'resources', 'invalid-xml-characters', 'requirements.txt'),
            '-o', os.path.join(dirname, 'bom.xml'),
        ])

        # assert
        with open(os.path.join(dirname, 'bom.xml'), 'rt') as f:
            actual_xml = f.read()
        assert actual_xml == expected_xml