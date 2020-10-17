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
import pytest
from cyclonedx.bom.generator import build_json_bom, build_xml_bom


script_path = os.path.dirname(__file__)


#TODO: update to use 1.2 spec
def test_xml_metadata_timestamp():
    # arrange
    with open(os.path.join(script_path, 'resources', 'valid-metadata-timestamp-1.2.xml'), 'r') as bf:
        expected_xml = bf.read()
    metadata = {
        'timestamp': '2020-04-07T07:01:00Z',
    }

    # act
    actual_xml = build_xml_bom([], metadata)

    # assert
    assert actual_xml == expected_xml

#TODO: update to use 1.2 spec
def test_json_metadata_timestamp():
    # arrange
    with open(os.path.join(script_path, 'resources', 'valid-metadata-timestamp-1.2.json'), 'r') as bf:
        expected_json = bf.read()
    metadata = {
        'timestamp': '2020-04-07T07:01:00Z',
    }

    # act
    actual_json = build_json_bom([], metadata)

    # assert
    assert actual_json == expected_json
