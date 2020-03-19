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
from cyclonedx.cli import read_bom
from cyclonedx.BomGenerator import build_bom

script_path = os.path.dirname(__file__)

def test_bom_generation():
    # arrange
    with open(os.path.join(script_path, 'resources', 'bom.xml'), 'r') as bf:
        expected_xml = bf.read()
    
    # act
    with open(os.path.join(script_path, 'resources', 'requirements.txt'), 'r') as fd:
        component_elements = read_bom(fd)
    
    actual_xml = build_bom(component_elements)

    # assert
    assert actual_xml == expected_xml
