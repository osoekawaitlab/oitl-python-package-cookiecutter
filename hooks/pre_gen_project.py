#!/usr/bin/env python3
"""Pre-generation hook for cookiecutter template."""

import subprocess
from pathlib import Path

# Get cookiecutter variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
GITHUB_INTEGRATION = "{{ cookiecutter.github_integration }}"

# Temporary file to share data between hooks
TEMP_FILE = Path("/tmp/cookiecutter_issue_info.txt")

ISSUE_TITLE = "[chore] Initial project setup"
ISSUE_BODY = f"""## Problem Statement

Starting a new Python package project requires establishing the foundational project structure, development tools, and configuration files.

## Proposed Solution

Set up the complete initial project structure including:

- Package structure with `src/` layout
- Testing framework and structure
- Development tools and task runners
- Documentation framework
- CI/CD pipeline configuration
- Project metadata and dependencies

## Acceptance Criteria

- [ ] `pyproject.toml` configured with package metadata and dependencies
- [ ] `src/` directory with package structure
- [ ] `tests/` directory with test framework setup
- [ ] Development task runner configured (`noxfile.py`)
- [ ] Documentation structure initialized (`docs/`, `mkdocs.yml`)
- [ ] GitHub workflows and issue templates configured (`.github/`)
- [ ] Python version specified (`.python-version`)
- [ ] Dependency lock file generated (`uv.lock`)
- [ ] All tests pass: `uv run nox -s tests`
- [ ] Code quality checks pass: `uv run nox -s mypy lint`
- [ ] Initial commit created and pushed

## Additional Context

This establishes the foundation for the `{PACKAGE_NAME}` package development.

### Getting Started

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run nox -s tests

# Run code quality checks
uv run nox -s mypy lint

# Build documentation locally
uv run nox -s docs_build
```

### Optional Post-Setup Tasks

- [ ] Configure GitHub repository settings (branch protection, required checks)
- [ ] Set up PyPI trusted publishing for automated releases
- [ ] Enable GitHub Pages for documentation deployment
- [ ] Configure code coverage reporting (e.g., Codecov)
- [ ] Add project-specific ADRs to `docs/adr/`
- [ ] Customize README with usage examples and badges
"""


def create_initial_issue():
    """Create an initial setup issue using gh CLI."""
    # Check if GitHub integration is enabled
    if GITHUB_INTEGRATION.lower() != "yes":
        print("GitHub integration disabled. Skipping issue creation.")
        return

    try:
        # Check if gh CLI is available
        subprocess.run(
            ["gh", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: gh CLI not found. Skipping issue creation.")
        print("You can manually create the initial setup issue later.")
        return

    try:
        # Check if we're in a git repository with a remote
        subprocess.run(
            ["git", "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        print("Warning: Not in a git repository with a remote.")
        print("Skipping issue creation. Run this after setting up the repository:")
        print(f'  gh issue create --title "{ISSUE_TITLE}" --body "$ISSUE_BODY"')
        return

    try:
        # Create the issue
        result = subprocess.run(
            ["gh", "issue", "create", "--title", ISSUE_TITLE, "--body", ISSUE_BODY],
            check=True,
            capture_output=True,
            text=True,
        )
        issue_url = result.stdout.strip()
        print(f"✓ Created initial setup issue: {issue_url}")

        # Save issue URL to temp file for post_gen_project hook
        try:
            TEMP_FILE.write_text(issue_url)
        except Exception as e:
            print(f"Warning: Failed to save issue info: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to create issue: {e.stderr}")
        print("You can manually create the issue later with:")
        print(f'  gh issue create --title "{ISSUE_TITLE}" --body-file issue.md')


if __name__ == "__main__":
    create_initial_issue()
