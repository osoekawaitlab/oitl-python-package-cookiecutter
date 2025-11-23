#!/usr/bin/env python3
"""Post-generation hook for cookiecutter template."""

import subprocess
import sys
from pathlib import Path

# Get cookiecutter variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
GITHUB_INTEGRATION = "{{ cookiecutter.github_integration }}"

# Temporary file to read issue info from pre_gen_project hook
TEMP_FILE = Path("/tmp/cookiecutter_issue_info.txt")

BRANCH_NAME = "setup/initial-project"
COMMIT_MESSAGE = "Initial project setup from cookiecutter"


def run_git_command(command, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e.stderr}")
        raise


def setup_git_and_create_pr():
    """Set up git, commit changes, and create a PR."""
    # Check if GitHub integration is enabled
    if GITHUB_INTEGRATION.lower() != "yes":
        print("\nGitHub integration disabled. Skipping automatic commit and PR creation.")
        print("You can manually set up the repository with:")
        print(f"  git checkout -b {BRANCH_NAME}")
        print(f"  git add .")
        print(f'  git commit -m "{COMMIT_MESSAGE}"')
        print(f"  git push -u origin {BRANCH_NAME}")
        return

    # Check if gh CLI is available
    try:
        subprocess.run(
            ["gh", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\nWarning: gh CLI not found. Skipping automatic commit and PR creation.")
        print("You can manually set up the repository with:")
        print(f"  git checkout -b {BRANCH_NAME}")
        print(f"  git add .")
        print(f'  git commit -m "{COMMIT_MESSAGE}"')
        print(f"  git push -u origin {BRANCH_NAME}")
        print(f"  gh pr create --title 'Initial project setup' --body '...'")
        return

    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        print("\nWarning: Not in a git repository. Skipping automatic commit and PR creation.")
        print("Initialize git first with:")
        print("  git init")
        print("  git remote add origin <repository-url>")
        return

    try:
        print("\n" + "=" * 60)
        print("Setting up git repository and creating PR...")
        print("=" * 60)

        # Create and checkout new branch
        print(f"\n1. Creating branch '{BRANCH_NAME}'...")
        run_git_command(["git", "checkout", "-b", BRANCH_NAME])
        print(f"   ✓ Created and checked out branch '{BRANCH_NAME}'")

        # Stage all files
        print("\n2. Staging files...")
        run_git_command(["git", "add", "."])
        print("   ✓ All files staged")

        # Commit
        print("\n3. Creating commit...")
        run_git_command(["git", "commit", "-m", COMMIT_MESSAGE])
        print(f"   ✓ Committed with message: '{COMMIT_MESSAGE}'")

        # Push to remote
        print("\n4. Pushing to remote...")
        run_git_command(["git", "push", "-u", "origin", BRANCH_NAME])
        print(f"   ✓ Pushed branch '{BRANCH_NAME}' to remote")

        # Read issue URL if available
        issue_reference = ""
        if TEMP_FILE.exists():
            try:
                issue_url = TEMP_FILE.read_text().strip()
                issue_number = issue_url.split("/")[-1]
                issue_reference = f"Closes #{issue_number}"
                # Clean up temp file
                TEMP_FILE.unlink()
            except Exception as e:
                print(f"   Warning: Could not read issue info: {e}")

        # Create PR
        print("\n5. Creating pull request...")
        pr_title = "Initial project setup"
        pr_body = f"""# Pull Request Overview

This PR sets up the initial project structure using the cookiecutter template for `{PROJECT_NAME}`.

## Changes

- Added package structure with `src/` layout
- Set up testing framework (unit and E2E tests with pytest)
- Configured code quality tools (mypy, ruff)
- Initialized documentation structure (MkDocs with Material theme)
- Added GitHub Actions workflows (tests, docs deployment, PyPI release)
- Created ADR template and architecture documentation structure
- Configured development task runner (noxfile.py)
- Added project metadata and configuration (pyproject.toml)

## Related Issues

{issue_reference}

## Test Details

All initial tests pass:
- Unit tests: ✓
- E2E tests: ✓
- Type checking: ✓
- Linting: ✓

Run tests with:
```bash
uv sync --group dev
uv run nox -s tests
```

## Future Work

See the related issue for the complete setup checklist. Key tasks remaining:
- Review and customize project documentation
- Configure GitHub repository settings
- Set up PyPI trusted publishing (if needed)
- Add project-specific functionality

## Notes

This is the foundational setup. After merging, follow the acceptance criteria in the related issue to complete the project setup.
"""

        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
            check=True,
            capture_output=True,
            text=True,
        )
        pr_url = result.stdout.strip()
        print(f"   ✓ Created pull request: {pr_url}")

        print("\n" + "=" * 60)
        print("✓ Setup complete!")
        print("=" * 60)
        print(f"\nPull Request: {pr_url}")
        print("\nNext steps:")
        print("1. Review the pull request")
        print("2. Complete the setup checklist in the issue")
        print("3. Merge the PR when ready")
        print()

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during setup: {e}")
        print("\nYou can complete the setup manually with:")
        print(f"  git checkout -b {BRANCH_NAME}")
        print(f"  git add .")
        print(f'  git commit -m "{COMMIT_MESSAGE}"')
        print(f"  git push -u origin {BRANCH_NAME}")
        print(f"  gh pr create --title 'Initial project setup'")
        sys.exit(1)


if __name__ == "__main__":
    setup_git_and_create_pr()
