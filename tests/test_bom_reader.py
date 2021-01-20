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

from cyclonedx.bom.reader import to_cpe


def test_to_cpe_success():
    result = to_cpe("cpe:2.3:a:ruamel.yaml_project:ruamel.yaml:0.1:*:*:*:*:*:*:*", "1.5.4")
    assert result == "cpe:2.3:a:ruamel.yaml_project:ruamel.yaml:1.5.4:*:*:*:*:*:*:*"

def test_to_cpe_success_simple_package():
    result = to_cpe("cpe:2.3:a:package:0.1:*:*:*:*:*:*:*", "2.0")
    assert result == "cpe:2.3:a:package:2.0:*:*:*:*:*:*:*"


def test_to_cpe_unknown_suffix():
    result = to_cpe("cpe:2.3:a:jenkins:docker:1.0.0:*:*:*:*:jenkins:*:*", "1.0.0")
    assert result is None


def test_to_cpe_unknown_prefix():
    result = to_cpe("cpe:5.0:a:jenkins:unspecified:1.0.0:*:*:*:*:*:*:*", "1.0.0")
    assert result is None
