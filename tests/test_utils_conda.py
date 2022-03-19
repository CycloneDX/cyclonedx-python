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

from cyclonedx_py.utils.conda import (
    CondaPackage,
    parse_conda_json_to_conda_package,
    parse_conda_list_str_to_conda_package,
)


class TestUtilsConda(TestCase):

    def test_parse_conda_json_no_hash(self) -> None:
        cp: CondaPackage = parse_conda_json_to_conda_package(
            conda_json_str='{"base_url": "https://repo.anaconda.com/pkgs/main","build_number": 1003,"build_string": '
                           '"py39hecd8cb5_1003","channel": "pkgs/main","dist_name": "chardet-4.0.0-py39hecd8cb5_1003",'
                           '"name": "chardet","platform": "osx-64","version": "4.0.0"}'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(1003, cp['build_number'])
        self.assertEqual('py39hecd8cb5_1003', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('chardet-4.0.0-py39hecd8cb5_1003', cp['dist_name'])
        self.assertEqual('chardet', cp['name'])
        self.assertEqual('osx-64', cp['platform'])
        self.assertEqual('4.0.0', cp['version'])
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_str_no_hash(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/osx-64/chardet-4.0.0-py39hecd8cb5_1003.conda'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(1003, cp['build_number'])
        self.assertEqual('py39hecd8cb5_1003', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('chardet-4.0.0-py39hecd8cb5_1003', cp['dist_name'])
        self.assertEqual('chardet', cp['name'])
        self.assertEqual('osx-64', cp['platform'])
        self.assertEqual('4.0.0', cp['version'])
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_str_with_hash_1(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/noarch/tzdata-2021a-h52ac0ba_0.conda'
                           '#d42e4db918af84a470286e4c300604a3'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(0, cp['build_number'])
        self.assertEqual('h52ac0ba_0', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('tzdata-2021a-h52ac0ba_0', cp['dist_name'])
        self.assertEqual('tzdata', cp['name'])
        self.assertEqual('noarch', cp['platform'])
        self.assertEqual('2021a', cp['version'], )
        self.assertEqual('d42e4db918af84a470286e4c300604a3', cp['md5_hash'])

    def test_parse_conda_list_str_with_hash_2(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/osx-64/ca-certificates-2021.7.5-hecd8cb5_1.conda'
                           '#c2d0ae65c08dacdcf86770b7b5bbb187'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(1, cp['build_number'])
        self.assertEqual('hecd8cb5_1', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('ca-certificates-2021.7.5-hecd8cb5_1', cp['dist_name'])
        self.assertEqual('ca-certificates', cp['name'])
        self.assertEqual('osx-64', cp['platform'])
        self.assertEqual('2021.7.5', cp['version'], )
        self.assertEqual('c2d0ae65c08dacdcf86770b7b5bbb187', cp['md5_hash'])

    def test_parse_conda_list_str_with_hash_3(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/noarch/idna-2.10-pyhd3eb1b0_0.tar.bz2'
                           '#153ff132f593ea80aae2eea61a629c92'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(0, cp['build_number'])
        self.assertEqual('pyhd3eb1b0_0', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('idna-2.10-pyhd3eb1b0_0', cp['dist_name'])
        self.assertEqual('idna', cp['name'])
        self.assertEqual('noarch', cp['platform'])
        self.assertEqual('2.10', cp['version'], )
        self.assertEqual('153ff132f593ea80aae2eea61a629c92', cp['md5_hash'])

    def test_parse_conda_list_str_with_hash_4(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://conda.anaconda.org/conda-forge/linux-64/_libgcc_mutex-0.1-conda_forge.tar.bz2'
                           '#d7c89558ba9fa0495403155b64376d81'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://conda.anaconda.org/conda-forge', cp['base_url'])
        self.assertIsNone(cp['build_number'])
        self.assertEqual('conda_forge', cp['build_string'])
        self.assertEqual('conda-forge', cp['channel'])
        self.assertEqual('_libgcc_mutex-0.1-conda_forge', cp['dist_name'])
        self.assertEqual('_libgcc_mutex', cp['name'])
        self.assertEqual('linux-64', cp['platform'])
        self.assertEqual('0.1', cp['version'])
        self.assertEqual('d7c89558ba9fa0495403155b64376d81', cp['md5_hash'])

    def test_parse_conda_list_build_number(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/osx-64/chardet-4.0.0-py39hecd8cb5_1003.conda'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(1003, cp['build_number'])
        self.assertEqual('py39hecd8cb5_1003', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('chardet-4.0.0-py39hecd8cb5_1003', cp['dist_name'])
        self.assertEqual('chardet', cp['name'])
        self.assertEqual('osx-64', cp['platform'])
        self.assertEqual('4.0.0', cp['version'])
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_no_build_number(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/linux-64/_libgcc_mutex-0.1-main.conda'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(None, cp['build_number'])
        self.assertEqual('main', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('_libgcc_mutex-0.1-main', cp['dist_name'])
        self.assertEqual('_libgcc_mutex', cp['name'])
        self.assertEqual('linux-64', cp['platform'])
        self.assertEqual('0.1', cp['version'])
        self.assertIsNone(cp['md5_hash'])

    def test_parse_conda_list_no_build_number2(self) -> None:
        cp: CondaPackage = parse_conda_list_str_to_conda_package(
            conda_list_str='https://repo.anaconda.com/pkgs/main/linux-64/_openmp_mutex-4.5-1_gnu.tar.bz2'
        )

        self.assertIsInstance(cp, dict)
        self.assertEqual('https://repo.anaconda.com/pkgs/main', cp['base_url'])
        self.assertEqual(None, cp['build_number'])
        self.assertEqual('1_gnu', cp['build_string'])
        self.assertEqual('pkgs/main', cp['channel'])
        self.assertEqual('_openmp_mutex-4.5-1_gnu', cp['dist_name'])
        self.assertEqual('_openmp_mutex', cp['name'])
        self.assertEqual('linux-64', cp['platform'])
        self.assertEqual('4.5', cp['version'])
        self.assertIsNone(cp['md5_hash'])
