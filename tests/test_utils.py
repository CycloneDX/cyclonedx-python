import pytest
from cyclonedx.model.component import Component
from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression
from cyclonedx_py._internal.utils.cdx import licenses_fixup

def test_single_expression_no_change():
    comp = Component(
        name="test-component",
        licenses=(LicenseExpression("MIT"),)
    )
    licenses_fixup(comp)
    assert comp.licenses[0].value == "MIT"
    assert comp.evidence is None

def test_multiple_named_no_change():
    comp = Component(
        name="test-component",
        licenses=(DisjunctiveLicense(name="MIT"),
                  DisjunctiveLicense(name="Apache-2.0"))
    )
    licenses_fixup(comp)
    names = {l.name for l in comp.licenses}
    assert names == {"MIT", "Apache-2.0"}
    assert comp.evidence is None

def test_expression_plus_named_moves_named_to_evidence():
    comp = Component(
        name="test-component",
        licenses=(LicenseExpression("MIT"),
                  DisjunctiveLicense(name="Apache-2.0"))
    )
    licenses_fixup(comp)
    # Check expression stays
    assert comp.licenses[0].value == "MIT"
    # Check named moved to evidence
    assert comp.evidence is not None
    moved = {l.name for l in comp.evidence.licenses}
    assert moved == {"Apache-2.0"}

def test_empty_licenses_no_change():
    comp = Component(
        name="test-component",
        licenses=()
    )
    licenses_fixup(comp)
    assert tuple(comp.licenses) == ()
    assert comp.evidence is None
