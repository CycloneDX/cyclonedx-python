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


"""
Functionality related to PEP 610.

See https://packaging.python.org/en/latest/specifications/direct-url/
See https://peps.python.org/pep-0610/
"""

from abc import ABC, abstractmethod
from json import JSONDecodeError, loads as json_loads
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from importlib.metadata import Distribution

    from cyclonedx.model import ExternalReference


class PackageSource(ABC):
    @abstractmethod
    def __init__(self, url: str) -> None:
        self.url = url


class PackageSourceVcs(PackageSource):
    # see https://packaging.python.org/en/latest/specifications/direct-url-data-structure/#vcs-urls

    def __init__(self, url: str,
                 vcs: str, requested_revision: Optional[str], commit_id: str) -> None:
        super().__init__(url)
        self.vcs = vcs
        self.requested_revision = requested_revision
        self.commit_id = commit_id

    @classmethod
    def from_data(cls, url: str, data: Dict[str, Any]) -> 'PackageSourceVcs':
        return cls(url, data['vcs'], data.get('requested_revision'), data['commit_id'])


class PackageSourceArchive(PackageSource):
    # see https://packaging.python.org/en/latest/specifications/direct-url-data-structure/#archive-urls

    def __init__(self, url: str,
                 hashes: Optional[Dict[str, str]]) -> None:
        super().__init__(url)
        self.hashes = hashes or {}

    @classmethod
    def from_data(cls, url: str, data: Dict[str, Any]) -> 'PackageSourceArchive':
        if 'hashes' in data:
            hashes = data['hashes']
        elif 'hash' in data:
            hash_parts = str(data['hash']).split('=', maxsplit=1)
            hashes = {hash_parts[0]: hash_parts[1]}
        else:
            hashes = None
        return cls(url, hashes)


class PackageSourceLocal(PackageSource):
    # see https://packaging.python.org/en/latest/specifications/direct-url-data-structure/#local-directories

    def __init__(self, url: str,
                 editable: bool) -> None:
        super().__init__(url)
        self.editable = editable

    @classmethod
    def from_data(cls, url: str, data: Dict[str, Any]) -> 'PackageSourceLocal':
        return cls(url, data.get('editable', False))


def packagesource4dist(dist: 'Distribution') -> Optional[PackageSource]:
    raw = dist.read_text('direct_url.json')
    if raw is None:
        return raw
    try:
        data = json_loads(raw)
    except JSONDecodeError:  # pragma: no cover
        return None
    url = data['url']
    if url == '':
        return None
    if 'vcs_info' in data:
        return PackageSourceVcs.from_data(url, data['vcs_info'])
    if 'archive_info' in data:
        return PackageSourceArchive.from_data(url, data['archive_info'])
    if 'dir_info' in data:
        return PackageSourceLocal.from_data(url, data['dir_info'])


def packagesource2extref(src: PackageSource) -> Optional['ExternalReference']:
    from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
    from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri
    try:
        if isinstance(src, PackageSourceVcs):
            return ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(f'{src.url}#{src.commit_id}'),
                comment=f'PackageSource: VCS {src.vcs!r}')
        if isinstance(src, PackageSourceArchive):
            hashes = []
            for hashlib_alg, content in src.hashes.items():
                try:
                    hashes.append(HashType.from_hashlib_alg(hashlib_alg, content))
                except UnknownHashTypeException:
                    pass
            return ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(src.url), hashes=hashes,
                comment='PackageSource: Archive')
        if isinstance(src, PackageSourceLocal):
            return ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(src.url),
                comment='PackageSource: Local')
    except InvalidUriException:
        pass
