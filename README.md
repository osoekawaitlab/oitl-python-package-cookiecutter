# oitl-python-package-cookiecutter

Cookiecutter template for Osoekawa IT Laboratory's Python packages.

## Features

This cookiecutter template provides a fully configured Python package structure with:

- Modern Python packaging with `pyproject.toml`
- Testing setup with pytest (unit and E2E tests)
- Code quality tools (mypy, ruff)
- Task automation with nox
- Documentation with MkDocs Material
- GitHub Actions workflows (tests, docs deployment, PyPI release)
- Architecture Decision Records (ADR) template
- VSCode settings
- **Fully automated setup** (with GitHub CLI):
  - Automatic issue creation with setup checklist
  - Automatic branch creation and commit
  - Automatic pull request creation

## Requirements

- Python 3.10 or higher
- [cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [uv](https://github.com/astral-sh/uv) (recommended)
- [GitHub CLI (gh)](https://cli.github.com/) (optional, required only if `github_integration=yes`)

## Usage

### Recommended Workflow (with GitHub CLI)

This is the recommended approach that fully automates the project setup:

```bash
# 1. Create a new GitHub repository and clone it
gh repo create myproject-py --public --clone

# 2. Navigate to the repository
cd myproject-py

# 3. Run cookiecutter from within the repository
cookiecutter /path/to/oitl-python-package-cookiecutter --output-dir .. --overwrite-if-exists
```

**Important:**
- When prompted for `project_slug`, enter the same name as your repository (e.g., `myproject-py`)
- When prompted for `github_integration`, select `yes` to enable automatic setup

**What happens automatically (when github_integration=yes):**

1. **Pre-generation hook** (`pre_gen_project`):
   - Creates an "Initial Project Setup" issue with a checklist of setup tasks

2. **Post-generation hook** (`post_gen_project`):
   - Creates a new branch `setup/initial-project`
   - Commits all generated files
   - Pushes the branch to GitHub
   - Creates a pull request linked to the setup issue

After cookiecutter completes, you'll have:
- ✅ An issue tracking setup tasks
- ✅ A pull request with the initial project structure
- ✅ Everything ready for review and merge

Simply review the PR, complete any remaining setup tasks from the issue checklist, and merge when ready!

**Note:** If you select `github_integration=no`, you'll need to manually set up git, commit, and push the files.

### Alternative: Standalone Project

You can also create a project without GitHub integration:

```bash
cookiecutter https://github.com/osoekawaitlab/oitl-python-package-cookiecutter
```

Or if you have cloned this repository locally:

```bash
cookiecutter /path/to/oitl-python-package-cookiecutter
```

### Configuration

You will be prompted for the following values:

- `project_name`: Human-readable project name (e.g., "My Project")
- `project_slug`: Repository name (auto-generated as `{project_name}-py`)
- `package_name`: Python package name (auto-generated from project_name)
- `project_description`: Short description of your project
- `author_name`: Your name
- `github_username`: Your GitHub username
- `github_organization`: GitHub organization (defaults to github_username)
- `python_version`: Default Python version for development (default: 3.12)
- `min_python_version`: Minimum supported Python version (default: 3.10)
- `license`: Choose from MIT, Apache-2.0, GPL-3.0, BSD-3-Clause
- `use_cli`: Include CLI support (yes/no)
- `github_integration`: Enable automatic GitHub setup (yes/no)
  - `yes`: Automatically create issue, branch, commit, and PR
  - `no`: Skip GitHub integration (manual setup required)

### After creating your project

**If you enabled GitHub integration (`github_integration=yes`):**
- You'll have a PR ready to review and merge
- Check the created issue for the setup checklist

**If you disabled GitHub integration (`github_integration=no`):**

```bash
cd {project_slug}
git init
git add .
git commit -m "Initial project setup"
git remote add origin <your-repo-url>
git push -u origin main

# Install dependencies and run tests
uv sync --group dev
uv run nox -s tests
```

## Project Structure

```
{project_slug}/
├── .github/
│   ├── workflows/          # CI/CD workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
├── docs/
│   ├── adr/                # Architecture Decision Records
│   └── architecture/       # Architecture documentation
├── src/{package_name}/     # Main package source code
├── tests/
│   ├── unit/               # Unit tests
│   └── e2e/                # End-to-end tests
├── pyproject.toml          # Project configuration
├── noxfile.py              # Task automation
└── mkdocs.yml              # Documentation configuration
```

## License

MIT
