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

import json
import sys
from json import JSONDecodeError
from typing import Optional, Tuple
from urllib.parse import urlparse

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class CondaPackage(TypedDict):
    """
    Internal package for unifying Conda package definitions to.
    """
    base_url: str
    build_number: Optional[int]
    build_string: str
    channel: str
    dist_name: str
    name: str
    platform: str
    version: str
    package_format: Optional[str]
    md5_hash: Optional[str]


def conda_package_to_purl(pkg: CondaPackage) -> PackageURL:
    """
    Return the purl for the specified package.
    See https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#conda
    """
    qualifiers = {
        'build': pkg['build_string'],
        'channel': pkg['channel'],
        'subdir': pkg['platform'],
    }
    if pkg['package_format'] is not None:
        qualifiers['type'] = str(pkg['package_format'])

    purl = PackageURL(
        type='conda', name=pkg['name'], version=pkg['version'], qualifiers=qualifiers
    )
    return purl


def parse_conda_json_to_conda_package(conda_json_str: str) -> Optional[CondaPackage]:
    try:
        package_data = json.loads(conda_json_str)
    except JSONDecodeError as e:
        raise ValueError(f'Invalid JSON supplied - cannot be parsed: {conda_json_str}') from e

    if not isinstance(package_data, dict):
        return None

    package_data.setdefault('package_format', None)
    package_data.setdefault('md5_hash', None)
    return CondaPackage(package_data)  # type: ignore # @FIXME write proper type safe dict at this point


def parse_conda_list_str_to_conda_package(conda_list_str: str) -> Optional[CondaPackage]:
    """
    Helper method for parsing a line of output from `conda list --explicit` into our internal `CondaPackage` object.

    Params:
        conda_list_str:
            Line of output from `conda list --explicit`

    Returns:
        Instance of `CondaPackage` else `None`.
    """

    line = conda_list_str.strip()

    if '' == line or line[0] in ['#', '@']:
        # Skip comments, @EXPLICT or empty lines
        return None

    # Remove any hash
    package_hash = None
    if '#' in line:
        *_line_parts, package_hash = line.split('#')
        line = ''.join(*_line_parts)

    package_parts = line.split('/')
    if len(package_parts) < 2:
        raise ValueError(f'Unexpected format in {package_parts}')
    *_package_url_parts, package_arch, package_name_version_build_string = package_parts
    package_url = urlparse('/'.join(_package_url_parts))

    package_name, build_version, build_string, package_format = split_package_string(package_name_version_build_string)
    build_string, build_number = split_package_build_string(build_string)

    return CondaPackage(
        base_url=package_url.geturl(), build_number=build_number, build_string=build_string,
        channel=package_url.path[1:], dist_name=f'{package_name}-{build_version}-{build_string}',
        name=package_name, platform=package_arch, version=build_version, package_format=package_format,
        md5_hash=package_hash
    )


def split_package_string(package_name_version_build_string: str) -> Tuple[str, str, str, str]:
    """Helper method for parsing package_name_version_build_string.

    Returns:
        Tuple (package_name, build_version, build_string)
    """
    package_nvbs_parts = package_name_version_build_string.split('-')
    if len(package_nvbs_parts) < 3:
        raise ValueError(f'Unexpected format in {package_nvbs_parts}')

    *_package_name_parts, build_version, build_string = package_nvbs_parts
    package_name = '-'.join(_package_name_parts)

    # Split package_format (.conda or .tar.gz) at the end
    _pos = build_string.find('.')
    package_format = build_string[_pos + 1:]
    build_string = build_string[0:_pos]

    return package_name, build_version, build_string, package_format


def split_package_build_string(build_string: str) -> Tuple[str, Optional[int]]:
    """Helper method for parsing build_string.

    Returns:
        Tuple (build_string, build_number)
    """

    if '' == build_string:
        return '', None

    if build_string.isdigit():
        return '', int(build_string)

    _pos = build_string.rindex('_') if '_' in build_string else -1
    if _pos >= 1:
        # Build number will be the last part - check if it's an integer
        # Updated logic given https://github.com/CycloneDX/cyclonedx-python-lib/issues/65
        build_number = build_string[_pos + 1:]
        if build_number.isdigit():
            return build_string, int(build_number)

    return build_string, None
