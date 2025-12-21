---
name: lint-pre-commit
description: Run linting and formatting checks with pre-commit; use when validating code quality before commits or reviews.
---

## Steps
1. Install dev requirements if needed: `pip install -r requirements-dev.txt`.
2. Run the full lint suite: `pre-commit run --all-files`.
3. Report any hook failures and suggest fixes or reruns.

## Notes
- If pre-commit is not installed, install it from the dev requirements.
