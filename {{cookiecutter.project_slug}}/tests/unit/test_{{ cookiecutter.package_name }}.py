"""Unit tests for {{ cookiecutter.package_name }} exports."""

import re

import {{ cookiecutter.package_name }}


def test_{{ cookiecutter.package_name }}_exports_version() -> None:
    """Test that {{ cookiecutter.package_name }} exports the correct version."""
    assert re.match(r"^\d+\.\d+\.\d+$", {{ cookiecutter.package_name }}.__version__)
