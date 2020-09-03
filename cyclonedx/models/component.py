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

class Component:
    def __init__(self,
        name=None,
        version=None,
        publisher=None,
        description=None,
        hashes=None,
        licenses=None,
        purl=None,
        modified=False,
        component_type='library'
    ):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.description = description
        self.hashes = [] if hashes is None else hashes
        self.licenses = [] if licenses is None else licenses
        self.purl = purl
        self.modified = modified
        self.component_type = component_type
