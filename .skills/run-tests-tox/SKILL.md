---
name: run-tests-tox
description: Run the test suite using tox when validating changes or preparing releases; use this for Python version matrix checks.
---

## Steps
1. Install dev requirements if needed: `pip install -r requirements-dev.txt`.
2. Run the test suite: `tox`.
3. Report failures with the failing envs and any relevant logs.

## Notes
- Use `tox -e py` to run the default Python env if you need a quick check.
