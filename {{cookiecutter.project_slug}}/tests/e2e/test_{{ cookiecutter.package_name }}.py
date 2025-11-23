"""End-to-end tests for {{ cookiecutter.package_name }}."""

import re
import subprocess


def test_{{ cookiecutter.package_name }}_prints_version() -> None:
    """Test that {{ cookiecutter.package_name }} prints the version."""
    result = subprocess.run(
        ["{{ cookiecutter.package_name }}", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert re.match(r"^\d+\.\d+\.\d+$", result.stdout.strip())
