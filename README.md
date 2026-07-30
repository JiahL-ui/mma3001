# MMA3001 — Workshop 1: Digital Data Management, Documentation, AI and Testing

This repository contains the organised deliverables for Workshop 1:
Git/GitHub workflow practice, a documented `matmul` algorithm with tests,
a Mermaid flowchart, and a `pdb` debugging exercise.

## Project structure

```
.
├── src/                   # Core, importable Python modules
│   └── matmul.py          # Pure-Python matmul + NumPy comparison + determinant
├── tests/                 # Pytest test suite
│   └── test_matmul.py     # Positive & negative test cases for matmul
├── tools/                 # Standalone scripts / utilities
│   ├── gps_plotter.py     # Bug-fixed GPS plotting script (pdb exercise)
│   └── upload_to_github.py# Script to sync this structure to GitHub
├── docs/                  # Documentation
│   ├── matmul_flowchart.md   # Mermaid flowchart of the matmul algorithm
│   ├── pdb_debug_report.md   # Root-cause report for the gps-plotter bug
│   └── test_report.html      # Generated pytest HTML report
├── data/                  # Data files (large/generated data is .gitignore'd)
├── examples/              # Example notebooks / usage demos
├── requirements.txt
├── setup.py
└── .gitignore
```

## Setup

```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest --html=docs/test_report.html --self-contained-html tests/test_matmul.py
```

## Generating documentation

```bash
pdoc src/matmul.py -o docs/pdoc
```

## What was cleaned up from the original notebook

The source notebook (`Workshop_01_2026.ipynb`) mixed teaching material,
duplicated code across cells (e.g. `matmul` and its tests were redefined
three separate times), and had a couple of runtime bugs in the final
upload cells (bare variable names inside f-strings that were never
defined, e.g. `f"/content/{mma3001}"`). This repo:

- Consolidates the `matmul` implementation into a single, tested module
  (`src/matmul.py`) with input validation and docstrings.
- De-duplicates the test cases into one pytest file with clear
  positive/negative sections.
- Extracts the flowchart and debugging write-up into standalone Markdown
  docs.
- Fixes the GitHub upload script so it actually runs (`tools/upload_to_github.py`).

## 🤖 AI Usage Statement

AI tools (Google Gemini, within Google Colab) were used responsibly
during the development of this project to assist with:

- **Code generation & refactoring** — drafting base code structure and
  optimising existing code.
- **Documentation & comments** — drafting inline comments, docstrings,
  and this README.
- **Debugging support** — suggesting potential causes and fixes when
  troubleshooting.

All AI-generated content was reviewed, verified, and edited by the
author to ensure accuracy, originality, and compliance with academic
integrity requirements. The author takes full responsibility for the
final content and quality of the code and documentation.
