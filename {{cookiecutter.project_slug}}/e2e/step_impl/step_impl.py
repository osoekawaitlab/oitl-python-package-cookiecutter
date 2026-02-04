"""Step implementations for Gauge tests."""

import importlib
import re

from getgauge.python import Messages, data_store, step

SEMVER_PATTERN = (
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


@step("Import the <package_name> package")
def import_package(package_name: str) -> None:
    """Import the specified package and verify it is imported successfully."""
    imported_module = importlib.import_module(package_name)
    assert imported_module is not None, f"Failed to import {package_name}"
    Messages.write_message(f"Successfully verified import of {package_name}")
    data_store.scenario["imported_module"] = imported_module


@step("Verify that <attr_name> follows the Semantic Versioning format")
def verify_version_format(attr_name: str) -> None:
    """Verify that the specified attribute follows Semantic Versioning."""
    imported_module = data_store.scenario["imported_module"]
    version_value = getattr(imported_module, attr_name, None)

    assert version_value is not None, f"Attribute {attr_name} not found in package."
    Messages.write_message(f"Detected Version: {version_value}")

    match = re.match(SEMVER_PATTERN, version_value)

    assert match is not None, f"Version '{version_value}' does not follow SemVer!"
