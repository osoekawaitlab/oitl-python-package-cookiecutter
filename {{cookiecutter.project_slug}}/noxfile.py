"""Nox configuration file for {{ cookiecutter.project_name }} project."""

import nox

nox.options.default_venv_backend = "uv"

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14"]


@nox.session(python="{{ cookiecutter.python_version }}")
def tests_unit(session: nox.Session) -> None:
    """Run unit tests only."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest", "tests/unit/", "-v")


@nox.session(python="{{ cookiecutter.python_version }}")
def tests_e2e(session: nox.Session) -> None:
    """Run E2E tests only."""
    session.install("-e", ".", "--group=dev")
    session.run("gauge", "validate", "e2e/specs")
    session.run("gauge", "run", "e2e/specs")



@nox.session(python="{{ cookiecutter.python_version }}")
def tests(session: nox.Session) -> None:
    """Run all tests with coverage reporting."""
    session.install("-e", ".", "--group=dev")
    session.run(
        "pytest",
        "--cov=src/{{ cookiecutter.package_name }}",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=80",
    )


@nox.session(python=PYTHON_VERSIONS)
def tests_all_versions(session: nox.Session) -> None:
    """Run all tests across all supported Python versions."""
    session.install("-e", ".", "--group=dev")
    session.run("pytest")


@nox.session(python="{{ cookiecutter.python_version }}")
def mypy(session: nox.Session) -> None:
    """Run mypy type checking."""
    session.install("-e", ".", "--group=dev")
    session.run("mypy", "src/", "tests/")


@nox.session(python="{{ cookiecutter.python_version }}")
def lint(session: nox.Session) -> None:
    """Run ruff linting."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "check", ".")


@nox.session(python="{{ cookiecutter.python_version }}")
def format_code(session: nox.Session) -> None:
    """Run ruff formatting."""
    session.install("-e", ".", "--group=dev")
    session.run("ruff", "format", ".")


@nox.session(python="{{ cookiecutter.python_version }}")
def docs_build(session: nox.Session) -> None:
    """Build documentation."""
    session.install("-e", ".", "--group=docs", "--group=dev")
    session.run("mkdocs", "build", "--strict")
