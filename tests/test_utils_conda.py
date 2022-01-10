# encoding: utf-8

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
from unittest import TestCase

from cyclonedx_py.utils.conda import parse_conda_json_to_conda_package, parse_conda_list_str_to_conda_package, \
    CondaPackage


class TestUtilsConda(TestCase):

    def test_parse_conda_json_no_hash(self) -> None:
        cp: CondaPackage = parse_conda_json_to_conda_package(
            conda_json_str='{"base_url": "https://repo.anaconda.com/pkgs/main","build_number": 1003,"build_string": '
                           '"py39hecd8cb5_1003","channel": "pkgs/main","dist_name": "chardet-4.0.0-py39hecd8cb5_1003",'
                           '"name": "chardet","platform": "osx-64","version": "4.0.0"}'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://repo.anaconda.com/pkgs/main')
        self.assertEqual(cp['build_number'], 1003)
        self.assertEqual(cp['build_string'], 'py39hecd8cb5_1003')
        self.assertEqual(cp['channel'], 'pkgs/main')
        self.assertEqual(cp['dist_name'], 'chardet-4.0.0-py39hecd8cb5_1003')
        self.assertEqual(cp['name'], 'chardet')
        self.assertEqual(cp['platform'], 'osx-64')
        self.assertEqual(cp['version'], '4.0.0')
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_str_no_hash(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/osx-64/chardet-4.0.0-py39hecd8cb5_1003.conda'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://repo.anaconda.com/pkgs/main')
        self.assertEqual(cp['build_number'], 1003)
        self.assertEqual(cp['build_string'], 'py39hecd8cb5_1003')
        self.assertEqual(cp['channel'], 'pkgs/main')
        self.assertEqual(cp['dist_name'], 'chardet-4.0.0-py39hecd8cb5_1003')
        self.assertEqual(cp['name'], 'chardet')
        self.assertEqual(cp['platform'], 'osx-64')
        self.assertEqual(cp['version'], '4.0.0')
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_str_with_hash_1(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/noarch/tzdata-2021a-h52ac0ba_0.conda'
                           '#d42e4db918af84a470286e4c300604a3'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://repo.anaconda.com/pkgs/main')
        self.assertEqual(cp['build_number'], 0)
        self.assertEqual(cp['build_string'], 'h52ac0ba_0')
        self.assertEqual(cp['channel'], 'pkgs/main')
        self.assertEqual(cp['dist_name'], 'tzdata-2021a-h52ac0ba_0')
        self.assertEqual(cp['name'], 'tzdata')
        self.assertEqual(cp['platform'], 'noarch')
        self.assertEqual(cp['version'], '2021a')
        self.assertEqual(cp['md5_hash'], 'd42e4db918af84a470286e4c300604a3')

    def test_parse_conda_list_str_with_hash_2(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/osx-64/ca-certificates-2021.7.5-hecd8cb5_1.conda'
                           '#c2d0ae65c08dacdcf86770b7b5bbb187'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://repo.anaconda.com/pkgs/main')
        self.assertEqual(cp['build_number'], 1)
        self.assertEqual(cp['build_string'], 'hecd8cb5_1')
        self.assertEqual(cp['channel'], 'pkgs/main')
        self.assertEqual(cp['dist_name'], 'ca-certificates-2021.7.5-hecd8cb5_1')
        self.assertEqual(cp['name'], 'ca-certificates')
        self.assertEqual(cp['platform'], 'osx-64')
        self.assertEqual(cp['version'], '2021.7.5')
        self.assertEqual(cp['md5_hash'], 'c2d0ae65c08dacdcf86770b7b5bbb187')

    def test_parse_conda_list_str_with_hash_3(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/noarch/idna-2.10-pyhd3eb1b0_0.tar.bz2'
                           '#153ff132f593ea80aae2eea61a629c92'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://repo.anaconda.com/pkgs/main')
        self.assertEqual(cp['build_number'], 0)
        self.assertEqual(cp['build_string'], 'pyhd3eb1b0_0')
        self.assertEqual(cp['channel'], 'pkgs/main')
        self.assertEqual(cp['dist_name'], 'idna-2.10-pyhd3eb1b0_0')
        self.assertEqual(cp['name'], 'idna')
        self.assertEqual(cp['platform'], 'noarch')
        self.assertEqual(cp['version'], '2.10')
        self.assertEqual(cp['md5_hash'], '153ff132f593ea80aae2eea61a629c92')

    def test_parse_conda_list_str_with_hash_4(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://conda.anaconda.org/conda-forge/linux-64/_libgcc_mutex-0.1-conda_forge.tar.bz2'
                           '#d7c89558ba9fa0495403155b64376d81'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual(cp['base_url'], 'https://conda.anaconda.org/conda-forge')
        self.assertIsNone(cp['build_number'])
        self.assertEqual(cp['build_string'], 'conda_forge')
        self.assertEqual(cp['channel'], 'conda-forge')
        self.assertEqual(cp['dist_name'], '_libgcc_mutex-0.1-conda_forge')
        self.assertEqual(cp['name'], '_libgcc_mutex')
        self.assertEqual(cp['platform'], 'linux-64')
        self.assertEqual(cp['version'], '0.1')
        self.assertEqual(cp['md5_hash'], 'd7c89558ba9fa0495403155b64376d81')
