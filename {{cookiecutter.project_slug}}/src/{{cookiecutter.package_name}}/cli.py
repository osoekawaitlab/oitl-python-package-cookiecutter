"""CLI module for {{ cookiecutter.package_name }}."""

from argparse import ArgumentParser

from {{ cookiecutter.package_name }}.core import __version__


def generate_cli_parser() -> ArgumentParser:
    """Generate the argument parser for the {{ cookiecutter.package_name }} CLI."""
    parser = ArgumentParser(
        description="{{ cookiecutter.project_description }}"
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main() -> None:
    """Entry point for the {{ cookiecutter.package_name }} command-line interface."""
    parser = generate_cli_parser()
    _ = parser.parse_args()
