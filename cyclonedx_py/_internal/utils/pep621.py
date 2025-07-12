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

"""
Functionality related to PEP 621.

See https://packaging.python.org/en/latest/specifications/declaring-project-metadata/
See https://peps.python.org/pep-0621/
"""

from base64 import b64encode
from collections.abc import Generator, Iterable, Iterator
from itertools import chain
from os.path import dirname, join
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any

from cyclonedx.exception.model import InvalidUriException
from cyclonedx.model import AttachedText, Encoding, ExternalReference, XsUri
from cyclonedx.model.component import Component
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement
from packaging.requirements import Requirement

from .cdx import url_label_to_ert
from .license_trove_classifier import is_license_trove, license_trove2spdx
from .mimetypes import guess_type

if TYPE_CHECKING:  # pragma: nocover
    from cyclonedx.factory.license import LicenseFactory
    from cyclonedx.model.component import ComponentType
    from cyclonedx.model.license import License


def classifiers2licenses(classifiers: Iterable[str], lfac: 'LicenseFactory',
                         lack: 'LicenseAcknowledgement'
                         ) -> Generator['License', None, None]:
    for c in classifiers:
        if is_license_trove(c):
            yield lfac.make_from_string(license_trove2spdx(c) or c,
                                        license_acknowledgement=lack)


def project2licenses(project: dict[str, Any], lfac: 'LicenseFactory',
                     gather_text: bool, *,
                     fpath: str) -> Generator['License', None, None]:
    lack = LicenseAcknowledgement.DECLARED
    if classifiers := project.get('classifiers'):
        # https://packaging.python.org/en/latest/specifications/pyproject-toml/#classifiers
        # https://peps.python.org/pep-0621/#classifiers
        # https://packaging.python.org/en/latest/specifications/core-metadata/#classifier-multiple-use
        yield from classifiers2licenses(classifiers, lfac, lack)
    if isinstance(plicense := project.get('license'), dict):
        # https://packaging.python.org/en/latest/specifications/pyproject-toml/#license
        # https://peps.python.org/pep-0621/#license
        # https://packaging.python.org/en/latest/specifications/core-metadata/#license
        if 'file' in plicense and 'text' in plicense:
            # per spec:
            # > These keys are mutually exclusive, so a tool MUST raise an error if the metadata specifies both keys.
            raise ValueError('`license.file` and `license.text` are mutually exclusive,')
        if len(plicense_file := plicense.get('file', '')) > 0:
            if gather_text:
                # Per PEP 621 spec:
                # > [...] a string value that is a relative file path [...].
                # > Tools MUST assume the file’s encoding is UTF-8.
                # But in reality, we found non-printable bytes in some files!
                with open(join(dirname(fpath), *PurePosixPath(plicense_file).parts), 'rb') as plicense_fileh:
                    content_type = guess_type(plicense_file) or AttachedText.DEFAULT_CONTENT_TYPE
                    yield DisjunctiveLicense(
                        name=f"declared license of '{project['name']}'",
                        acknowledgement=lack,
                        text=AttachedText(
                            content_type=content_type,
                            encoding=Encoding.BASE_64,
                            content=b64encode(
                                plicense_fileh.read()
                            ).decode('ascii')))
        elif len(plicense_text := plicense.get('text', '')) > 0:
            license = lfac.make_from_string(plicense_text, license_acknowledgement=lack)
            if isinstance(license, DisjunctiveLicense) and license.id is None:
                if gather_text:
                    # per spec, `License` is either a SPDX ID/Expression, or a license text(not name!)
                    yield DisjunctiveLicense(
                        name=f"declared license of '{project['name']}'",
                        acknowledgement=lack,
                        text=AttachedText(content=plicense_text))
            else:
                yield license
    # Silently skip any other types (including string/PEP 639)


def project2extrefs(project: dict[str, Any]) -> Generator['ExternalReference', None, None]:
    # see https://packaging.python.org/en/latest/specifications/pyproject-toml/#urls
    for label, url in project.get('urls', {}).items():
        try:
            yield ExternalReference(
                comment=f'from pyproject urls: {label}',
                type=url_label_to_ert(label),
                url=XsUri(str(url)))
        except InvalidUriException:  # pragma: nocover
            pass


def project2component(project: dict[str, Any], *,
                      ctype: 'ComponentType') -> 'Component':
    dynamic = project.get('dynamic', ())
    return Component(
        type=ctype,
        name=project['name'],
        version=project.get('version', None) if 'version' not in dynamic else None,
        description=project.get('description', None) if 'description' not in dynamic else None,
        external_references=project2extrefs(project),
        # licenses are not gathered here per default, they may be sourced otherwise
        # TODO add more properties according to spec
    )


def project2dependencies(project: dict[str, Any]) -> Iterator['Requirement']:
    return (
        Requirement(dep)
        for dep in chain(
            project.get('dependencies', ()),
            chain.from_iterable(project.get('optional-dependencies', {}).values())
        )
    )
