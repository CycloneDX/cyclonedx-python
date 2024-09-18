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


from unittest import TestCase

from cyclonedx.spdx import is_supported_id
from ddt import ddt, named_data

from cyclonedx_py._internal.utils.license_trove_classifier import __TO_SPDX_MAP as TO_SPDX_MAP


@ddt
class TestLicenseTroveClassifier(TestCase):

    @named_data(*TO_SPDX_MAP.items())
    def test_map_is_known_id(self, mapped: str) -> None:
        self.assertTrue(is_supported_id(mapped))
