import pytest
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression
from cyclonedx.schema import SchemaVersion
from cyclonedx_py._internal.utils.cdx import licenses_fixup


def attach_schema(comp: Component, version: SchemaVersion):
    """Attach a BOM with a specific schema version to a component."""
    bom = Bom()
    bom.metadata.schema_version = version
    comp._bom = bom





def test_legacy_single_expression_no_change():
    comp = Component(name="c", licenses=(LicenseExpression("MIT"),))
    attach_schema(comp, SchemaVersion.V1_6)

    licenses_fixup(comp)

    assert comp.licenses[0].value == "MIT"
    assert comp.evidence is None


def test_legacy_multiple_named_no_change():
    comp = Component(
        name="c",
        licenses=(DisjunctiveLicense(name="MIT"), DisjunctiveLicense(name="Apache-2.0"))
    )
    attach_schema(comp, SchemaVersion.V1_6)

    licenses_fixup(comp)

    assert {l.name for l in comp.licenses} == {"MIT", "Apache-2.0"}
    assert comp.evidence is None


def test_legacy_expression_plus_named_moves_to_evidence():
    comp = Component(
        name="c",
        licenses=(LicenseExpression("MIT"), DisjunctiveLicense(name="Apache-2.0"))
    )
    attach_schema(comp, SchemaVersion.V1_6)

    licenses_fixup(comp)

    assert comp.licenses[0].value == "MIT"
    assert comp.evidence is not None
    assert {l.name for l in comp.evidence.licenses} == {"Apache-2.0"}


def test_legacy_empty_licenses_no_change():
    comp = Component(name="c", licenses=())
    attach_schema(comp, SchemaVersion.V1_6)

    licenses_fixup(comp)

    assert tuple(comp.licenses) == ()
    assert comp.evidence is None




def test_modern_no_fixup_mixed_is_untouched():
    comp = Component(
        name="c",
        licenses=(LicenseExpression("MIT"), DisjunctiveLicense(name="Apache-2.0"))
    )
    attach_schema(comp, SchemaVersion.V1_7)

    licenses_fixup(comp)

    # Mixed licenses must not be modified
    assert len(comp.licenses) == 2
    assert comp.evidence is None


def test_modern_named_only_untouched():
    comp = Component(
        name="c",
        licenses=(DisjunctiveLicense(name="MIT"), DisjunctiveLicense(name="Apache-2.0")),
    )
    attach_schema(comp, SchemaVersion.V1_7)

    licenses_fixup(comp)

    assert {l.name for l in comp.licenses} == {"MIT", "Apache-2.0"}
    assert comp.evidence is None


def test_modern_expression_only_untouched():
    comp = Component(
        name="c",
        licenses=(LicenseExpression("MIT"),),
    )
    attach_schema(comp, SchemaVersion.V1_7)

    licenses_fixup(comp)

    assert comp.licenses[0].value == "MIT"
    assert comp.evidence is None
