# FAST — Federal Advocacy Support Toolkit

FAST (Federal Advocacy Support Toolkit) is a lightweight Python toolkit for generating and rendering advocacy materials (arguments, issue renders, audio rendering helpers, and related workflows). The repository contains scripts and utilities for building outputs for different federal advocacy scenarios. The tool is tailored to NTEU/IRS grievance.

Status
- Public repo
- Language: Python
- This README provides a quick-start, developer guidance, and recommended next steps.

Table of Contents
- About
- Features
- Quick Start
  - Requirements
  - Install
  - Run examples
- Structure
- Development
  - Dev container
  - Tests and CI
  - Linting and formatting
- Packaging and distribution
- Files and assets
- Security
- License
- Contact

About
FAST aims to provide reusable utilities to help generate argument text and render themed outputs (annual issues, furlough notices, abeyance, AWOL-related formatting, and audio helpers). The codebase is organized as a set of scripts and a util module. This README will help you get started and maintain the project.

Features
- Argument generation scripts (annual, measurable/unmeasurable)
- Rendering scripts for several issue types (awol, furlough, abeyance, annual)
- Audio helper utilities and an audio directory for samples/assets
- A devcontainer to streamline onboarding in VS Code

Quick Start

Requirements
- Python 3.10+ recommended (3.8+ likely works)
- Git
- (Optional) VS Code with Remote - Containers for devcontainer support

Clone
```bash
git clone https://github.com/mhoffman88/FAST.git
cd FAST
```

Create a virtual environment and install dependencies
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Run help/inspect entry script
```bash
python fast_main.py --help
# or inspect specific scripts
python render_annual_issue.py --help
```

Example runs
Note: the scripts currently accept different CLI arguments; use `--help` to see available flags.

- Render an annual issue (example)
```bash
python render_annual_issue.py --input examples/annual_input.json --output out/annual.md
```

- Create argument text
```bash
python annual_arguments.py --source data/some_input.json --out out/arguments.txt
```

Replace file names and flags with the appropriate arguments supported by each script.

Project structure (top-level)
- .devcontainer/ — VS Code/devcontainer configuration (useful for onboarding)
- NTEU-logo.png — project logo (large binary; see "Files and assets")
- annual_arguments.py — generation logic for annual arguments
- meas_unmeas_arguments.py — generation for measurable/unmeasurable arguments
- render_abeyance.py — renderer for abeyance outputs
- render_annual_issue.py — renderer for annual issue outputs
- render_awol_issue.py — renderer for AWOL-related outputs
- render_furlough.py — renderer for furlough outputs
- render_audio.py — audio rendering helper/entry
- fast_main.py — primary entry/launcher script (inspect for flags)
- util.py — shared utility functions used by render and argument scripts
- audio/ — audio assets (samples)
- requirements.txt — Python dependencies

Development

Dev container
If you use VS Code, open the repository in the Remote - Containers extension or use "Reopen in Container" so you get a consistent environment based on the .devcontainer configuration.

Tests
- There are currently no tests in the repository. Add pytest-based tests in a tests/ directory.
- Minimal test commands:
```bash
pip install pytest
pytest
```
- Aim to test pure logic functions (argument generation and render formatting) independently of file I/O.

CI (recommended)
- Add a GitHub Actions workflow that:
  - Installs dependencies
  - Runs static checks (ruff/flake8)
  - Runs black for formatting (or use pre-commit)
  - Runs pytest
- I can scaffold a starter .github/workflows/python-ci.yml if you'd like.

Linting and formatting
- Recommended tools:
  - black (formatting)
  - ruff or flake8 (linting)
  - isort (imports)
  - mypy (static typing)
  - pre-commit (hook integration)
- Example pre-commit flow:
```yaml
repos:
- repo: https://github.com/psf/black
  rev: stable
  hooks: [{id: black}]
- repo: https://github.com/charliermarsh/ruff
  rev: stable
  hooks: [{id: ruff}]
- repo: https://github.com/pre-commit/mirrors-isort
  rev: v5.12.0
  hooks: [{id: isort}]
```

Packaging and entry points
- To make FAST installable:
  - Move scripts into a package directory (e.g., fast/ or fast_toolkit/)
  - Add pyproject.toml (Poetry or setuptools) and configure a console_scripts entry point (e.g., fast=fast.__main__:main)
- This makes installation via pip straightforward: `pip install .`

Files and assets
- NTEU-logo.png is large (~2.1 MB). If you expect many binary assets or larger audio files:
  - Use Git LFS or store large assets in releases or cloud storage.
  - Keep small sample assets in repo for examples and tests only.
- Avoid committing secrets or credentials. If any accidentally got committed, rotate them immediately and remove them from history.

License
This project is released under the MIT License. See the LICENSE file for details.


Contact / Maintainer
- Maintainer: @mhoffman88
- Repo: https://github.com/mhoffman88/FAST
