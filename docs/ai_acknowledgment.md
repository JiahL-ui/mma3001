# AI Acknowledgment

This document records how Artificial Intelligence tools were used during
the development of this project, in accordance with
[Monash University's guidelines on acknowledging AI use](https://www.monash.edu/student-academic-success/learning-with-ai/academic-integrity-and-ai/acknowledging-the-use-of-ai).

---

## Tools Used

| Tool | Purpose |
|------|---------|
| GitHub Copilot (VS Code) | Code generation, docstring writing, refactoring, debugging |
| Google Gemini 2.5 (Colab) | Notebook formatting, example generation, flowchart scripting |

## Areas of AI Assistance

### 1. Code Generation & Refactoring
- Generated the initial `matmul()` pure-Python implementation with input validation.
- Refactored duplicated notebook cells into a single importable `src/matmul.py` module.
- Created the pytest test suite (`tests/test_matmul.py`) with positive and negative test cases.

### 2. Documentation & Docstrings
- Used Google-style and NumPy-style docstrings for all public functions in `src/matmul.py`.
- Generated the Mermaid flowchart script for the `matmul` algorithm in `docs/matmul_flowchart.md`.
- Produced the pdb debugging report (`docs/pdb_debug_report.md`) documenting the GPS plotting bug root cause.

### 3. Debugging & Problem Solving
- Assisted in identifying the floating-point precision drift bug in `gps-plotter.py` via `pdb`.
- Suggested `numpy.clip()` as the fix and helped integrate it into the fixed `tools/gps_plotter.py`.

### 4. Automation & Tooling
- Generated `tools/build_docs.py` to automate pdoc, pytest, and documentation builds.
- Helped configure `setup.py` and `requirements.txt` for the project.

---

## Review & Verification

All AI-generated content has been:
- Reviewed for correctness and accuracy.
- Modified where necessary to fit project requirements.
- Tested (code has been run and verified with pytest).

The project author(s) take full responsibility for the final code and documentation quality.

---

*Last updated: 2026-07-30*
