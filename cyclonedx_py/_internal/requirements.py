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


from argparse import OPTIONAL, ArgumentParser
from collections.abc import Generator, Iterable
from functools import reduce
from itertools import chain
from os import unlink
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Optional

from cyclonedx.exception.model import InvalidUriException, UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, Property, XsUri
from cyclonedx.model.component import Component, ComponentType
from packageurl import PackageURL
from pip_requirements_parser import RequirementsFile  # type:ignore[import-untyped]

from . import BomBuilder, PropertyName, PurlTypePypi
from .cli_common import add_argument_mc_type, add_argument_pyproject
from .utils.cdx import make_bom
from .utils.io import io2file
from .utils.packaging import normalize_packagename
from .utils.pyproject import pyproject_file2component
from .utils.secret import redact_auth_from_url

if TYPE_CHECKING:  # pragma: no cover
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from pip_requirements_parser import InstallRequirement


class RequirementsBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        p = ArgumentParser(
            description=dedent("""\
                Build an SBOM from Pip requirements.

                The options and switches mimic the respective ones from Pip CLI.
                """),
            epilog=dedent("""\
                Example Usage:
                  • Build an SBOM from a requirements file:
                      $ %(prog)s requirements-prod.txt
                  • Merge multiple files and build an SBOM from it:
                      $ cat requirements/*.txt | %(prog)s -
                  • Build an inventory for all installed packages:
                      $ python -m pip freeze --all | %(prog)s -
                  • Build an inventory for all installed packages in a conda environment:
                      $ conda run python -m pip freeze --all | %(prog)s -
                  • Build an inventory for installed packages in a Python (virtual) environment:
                      $ .../.venv/bin/python -m pip freeze --all --local --require-virtualenv | \\
                        %(prog)s -
                  • Build an inventory from an unfrozen manifest:
                      $ python -m pip install -r dependencies.txt && \\
                        python -m pip freeze | %(prog)s -
               """),
            **kwargs)
        # the options and switches SHALL mimic the ones from Pip
        p.add_argument('-i', '--index-url',
                       metavar='<url>',
                       help='Base URL of the Python Package Index. '
                            'This should point to a repository compliant with PEP 503 (the simple repository API) '
                            'or a local directory laid out in the same format.'
                            ' (default: %(default)s)',
                       dest='index_url',
                       default='https://pypi.org/simple')
        p.add_argument('--extra-index-url',
                       metavar='<url>',
                       help='Extra URLs of package indexes to use in addition to --index-url. '
                            'Should follow the same rules as --index-url',
                       action='append',
                       dest='extra_index_urls',
                       default=[])
        add_argument_pyproject(p)
        add_argument_mc_type(p)
        p.add_argument('requirements_file',
                       metavar='<requirements-file>',
                       help='Path to requirements file. May be set to "-" to read from <stdin>.'
                            ' (default: %(default)r in current working directory)',
                       nargs=OPTIONAL,
                       default='requirements.txt')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 index_url: str,
                 extra_index_urls: Iterable[str],
                 **__: Any) -> None:
        self._logger = logger
        self._index_url = index_url
        self._extra_index_urls = tuple(extra_index_urls)

    def __call__(self, *,  # type:ignore[override]
                 requirements_file: str,
                 pyproject_file: Optional[str],
                 mc_type: 'ComponentType',
                 **__: Any) -> 'Bom':
        if pyproject_file is None:
            rc = None
        else:
            rc = pyproject_file2component(pyproject_file, ctype=mc_type,
                                          gather_license_texts=False, logger=self._logger)
            rc.bom_ref.value = 'root-component'

        if requirements_file == '-':
            from sys import stdin  # late bind, to allow patching
            rt = io2file(stdin.buffer)
            try:
                rf = RequirementsFile.from_file(rt, include_nested=False)
            finally:
                unlink(rt)
            del rt, stdin
        else:
            rf = RequirementsFile.from_file(requirements_file, include_nested=True)

        return self._make_bom(rc, rf)

    def _make_bom(self, root_c: Optional['Component'], rf: 'RequirementsFile') -> 'Bom':
        bom = make_bom()
        bom.metadata.component = root_c
        self._logger.debug('root-component: %r', root_c)
        self._add_components(bom, rf)

        return bom

    def _add_components(self, bom: 'Bom', rf: 'RequirementsFile') -> None:
        index_url = redact_auth_from_url(reduce(
            lambda c, i: i.options.get('index_url') or c, rf.options, self._index_url
        ).rstrip('/'))
        extra_index_urls = frozenset(map(
            lambda u: redact_auth_from_url(u.rstrip('/')),
            chain(self._extra_index_urls, chain.from_iterable(
                i.options['extra_index_urls'] for i in rf.options if 'extra_index_urls' in i.options
            ))
        ))
        self._logger.debug('index_url = %r', index_url)
        self._logger.debug('extra_index_urls = %r', extra_index_urls)

        for requirement in rf.requirements:
            component = self._make_component(requirement, index_url, extra_index_urls)
            self._logger.info('add component for line %r', requirement.line)
            self._logger.debug('add component: %r', component)
            if not component.version and not requirement.is_url:
                self._logger.warning('component has no pinned version: %r', component)
            bom.components.add(component)

    def __hashes4req(self, req: 'InstallRequirement') -> Generator['HashType', None, None]:
        for hash in req.hash_options:
            try:
                yield HashType.from_composite_str(hash)
            except UnknownHashTypeException as error:
                self._logger.debug('skipping hash %s', hash, exc_info=error)
                del error

    def _make_component(self, req: 'InstallRequirement',
                        index_url: str, extra_index_urls: frozenset[str]) -> 'Component':
        name = req.name
        version = req.get_pinned_version or None
        hashes = list(self.__hashes4req(req))
        external_references = []
        purl_qualifiers = {}  # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst

        # workaround for https://github.com/nexB/pip-requirements-parser/issues/24
        is_local = req.is_local_path and (not req.link or req.link.scheme in ['', 'file'])
        try:
            if is_local:
                external_references.append(ExternalReference(
                    comment='explicit local path',
                    type=ExternalReferenceType.OTHER,
                    url=XsUri(req.link.url),
                    hashes=hashes))
            elif req.is_url:
                if '://files.pythonhosted.org/' not in req.link.url:
                    # skip PURL bloat, do not add implicit information
                    purl_qualifiers['vcs_url' if req.is_vcs_url else 'download_url'] = redact_auth_from_url(
                        req.link.url)
                external_references.append(ExternalReference(
                    comment='explicit dist url',
                    type=ExternalReferenceType.VCS if req.is_vcs_url else ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(redact_auth_from_url(req.link.url)),
                    hashes=hashes))
            else:
                # url based on https://warehouse.pypa.io/api-reference/legacy.html
                external_references.append(ExternalReference(
                    comment='implicit dist url',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(f'{index_url or self._index_url}/{name}/'),
                    hashes=hashes))
                for eiurl in extra_index_urls:
                    external_references.append(ExternalReference(
                        comment='implicit dist extra-url',
                        type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(f'{eiurl}/{name}/'),
                        hashes=hashes))
        except InvalidUriException as error:
            self._logger.debug('failed ExternalReference/url URL for: %s', req.line, exc_info=error)
            del error

        return Component(
            bom_ref=f'requirements-L{req.line_number}',
            description=f'requirements line {req.line_number}: {redact_auth_from_url(req.line)}',
            type=ComponentType.LIBRARY,
            name=name or 'unknown',
            version=version,
            purl=PackageURL(
                type=PurlTypePypi,
                name=req.name,
                version=version,
                qualifiers=purl_qualifiers
            ) if not is_local and name else None,
            external_references=external_references,
            properties=(Property(
                name=PropertyName.PythonPackageExtra.value,
                value=normalize_packagename(extra)
            ) for extra in req.extras)
        )
