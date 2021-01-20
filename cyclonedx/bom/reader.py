import re
import requests
import requirements
from collections import OrderedDict
from packageurl import PackageURL
from packaging.utils import canonicalize_version
from packaging.version import parse as packaging_parse

from cyclonedx.bom import generator
from cyclonedx.models import *


DEFAULT_PACKAGE_INFO_URL = "https://pypi.org/pypi/{package_name}/{package_version}/json"

def read_bom(fd, package_info_url=DEFAULT_PACKAGE_INFO_URL, json=False, nvd_cpe=False):
    """Read BOM data from file handle."""

    print("Generating CycloneDX BOM")
    all_components = (get_component(req, package_info_url, nvd_cpe) for req in requirements.parse(fd))

    # there can be duplicates in all_components, get rid of them
    components = []
    added_purls = []
    for component in all_components:
        if component is not None and component.purl not in added_purls:
            components.append(component)
            added_purls.append(component.purl)

    if json:
        bom = generator.build_json_bom(components)
    else:
        bom = generator.build_xml_bom(components)
    
    return bom


def get_component(req, package_info_url=DEFAULT_PACKAGE_INFO_URL, nvd_cpe=False):
    if req.local_file:
        print("WARNING: Local file " + req.path + " does not have versions. Skipping.")
        return None

    if not req.specs:
        print("WARNING: " + req.name + " does not have a version specified. Skipping.")
        return None

    if len(req.specs[0]) < 2:
        # TODO is this even possible?
        return None

    # set defaults
    component = Component(
        name=req.name,
        version=req.specs[0][1],
        purl=generate_purl(req.name, req.specs[0][1]),
        component_type='library'
    )

    if req.specs[0][0] != "==":
        print('WARNING: {component.name} is not pinned to a specific version. Using: {component.version}'.format(component=component))

    if nvd_cpe:
        cpe = match_cpe_from_nvd(req.name, req.specs[0][1])
        if cpe:
            component.cpe = cpe
        else:
            print("WARNING: Failed to match CPE for {component.name}".format(component=component))

    package_info = get_package_info(component.name, component.version, package_info_url)
    if package_info:
        component.publisher = package_info["info"]["author"]
        component.description = package_info["info"]["summary"]
        # TODO: Attempt to perform SPDX license ID resolution
        package_license = package_info["info"]["license"]
        if package_license and package_license != 'UNKNOWN' and len(package_license.strip()) > 0:
            license = License(name=package_license)
            component_license = ComponentLicense(license=license)
            component.licenses.append(component_license)

        if component.version in package_info["releases"]:
            release_info = get_release_info(package_info, component.version)
            component.hashes = get_hashes(release_info)
            component.hashes.sort()
        else:
            print('WARNING: {component.name}=={component.version} could not be found in PyPi'.format(component=component))

    return component


def get_package_info(
        package_name,
        package_version,
        url=DEFAULT_PACKAGE_INFO_URL,
):
    url = url.format(package_name=package_name, package_version=package_version)

    try:
        request_data = requests.get(url)
        request_data.raise_for_status()
        package_info = request_data.json()
    except requests.RequestException:
        print("WARNING: could not retrieve package info for " + package_name)
        package_info = None

    return package_info


def generate_purl(package_name, package_version):
    return PackageURL("pypi", '', package_name, package_version, '', '').to_string()


def match_cpe_from_nvd(package_name, package_version):
    """
    Search the NIST National Vulnerabilities Database for matches to the pip dependency.

    NIST publishes CVEs in the NVD (National Vulnerability Database) using CPE
    (Common Platform Enumeration). A CPE, like a PURL, is used to uniquely identify
    a dependency — but is intended for software/hardware typically not libraries.

    Unfortunately, python CPEs do not seem to have a completely predictable pattern.
    NIST exposes a REST endpoint where this method will attempt to search for a matching
    CPE for the given package.

    Including a CPE in the Bill of Materials for a Python dependency can result in
    more thorough CVE matching in tools such as OWASP Dependency Track.
    """

    # It should be sufficient to find the first match (if any) - hence resultsPerPage=1.
    # If any CPE matches the package name, the version will be substituted into the
    # cpe returned by this method.
    nvd_url = "https://services.nvd.nist.gov/rest/json/cpes/1.0"
    params = {"cpeMatchString": "cpe:2.3:a:*:{package_name}".format(package_name=package_name),
              "resultsPerPage": 1}
    response = requests.get(url=nvd_url, params=params)

    # The response will be JSON
    nvd_results = response.json()
    result = nvd_results['result']

    # Look for a cpe entry
    if result and result['cpes']:
        cpe_match = result['cpes'][0]
        if cpe_match:
            cpe23Uri = cpe_match['cpe23Uri']

            if cpe23Uri:
                return to_cpe(cpe23Uri, package_version)

    return None


def to_cpe(cpe23Uri, package_version):
    """
    A cpe23Uri will look something like "cpe:2.3:a:ruamel.yaml_project:ruamel.yaml:0.1:*:*:*:*:*:*:*"
    when matching against `ruamel_yaml`. This is close, but the version must be replaced with the
    package version we are interested in.

    This is done because the NVD does not always have a CPE that matches the exact version of every
    python dependency for which it has an entry.
    """

    pat = re.compile(r"(?P<prefix>cpe:2.3:a:)(?P<package>.*:)(?P<version>.*:)(?P<suffix>\*:\*:\*:\*:\*:\*:\*)")
    (result, count) = pat.subn(r"\g<prefix>\g<package>" + package_version + r":\g<suffix>", cpe23Uri)
    if count == 1:
        return result
    return None


def translate_digests(digests):
    mapping = {
        'md5': 'MD5',
        'sha1': 'SHA-1',
        'sha256': 'SHA-256',
        'sha512': 'SHA-512',
    }
    return [Hash(mapping[k], digests[k]) for k in digests if k in mapping]


def _get_pypi_version(special_version, release_dict):
    """
    Loop over the pypi release dictionary looking for an equivalent version string. Return the alternative version
    if found, otherwise return None.
    :param special_version: The version string that failed to match against the Pypi versions.
    :param release_dict: Pypi's releases dictionary for a given module.
    :return: The matching version string or None if it not matched.
    """
    for release in release_dict:
        pypi_version = canonicalize_version(release)
        if special_version == pypi_version or special_version == release:
            return release
    return None


def get_release_info(package_info, specified_version):
    releases_info = package_info["releases"]
    release_info = releases_info.get(specified_version)
    parsed_version = packaging_parse(specified_version)
    if parsed_version.is_prerelease or parsed_version.is_postrelease or parsed_version.is_devrelease:
        pypi_version = _get_pypi_version(specified_version, releases_info)
        if pypi_version:
            release_info = releases_info[pypi_version]
        else:
            # Unable to find a matching normalized version string, throw exception
            raise ValueError("Could not find a matching normalized version string", package_info['name'], specified_version)
    return release_info


def get_hashes(releases):
    # TODO: include version that would get installed on this system
    #       now has hashes from arbitrary distribution (multiple wheels possible)
    has_wheel = any(r["packagetype"] == "bdist_wheel" for r in releases)

    # pip will always prefer bdist_wheel over sdist - therefore hashes from bdist_wheel take precedence
    relevant_releases = []
    for r in releases:
        if has_wheel and r["packagetype"] == "bdist_wheel" or not has_wheel and r["packagetype"] == "sdist":
            relevant_releases.append(r)

    # instead of doing something like this once the TODO above is complete...
    # hashes = []
    # for release in relevant_releases:
    #     hashes.extend(translate_digests(release['digests']))

    # doing this to mimic current behaviour of picking the last hash
    hashes = {}
    for release in relevant_releases:
        release_hashes = translate_digests(release['digests'])
        for release_hash in release_hashes:
            hashes[release_hash.alg] = release_hash

    return [hashes[k] for k in hashes]
