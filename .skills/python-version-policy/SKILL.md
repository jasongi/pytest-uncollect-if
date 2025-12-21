---
name: python-version-policy
description: Update project metadata for supported Python versions, adjust minimum Python requirement and classifiers, and document versioning policy when Python releases or EOL changes occur.
---

## Purpose
Use this skill when a repo needs its supported Python versions refreshed after a new Python release or when dropping EOL versions.

## Steps
1. Check the upstream Python version status list and identify supported branches.
2. Update the project metadata (minimum Python, classifiers, CI/tox versions) to match supported versions.
3. Run the test suite with tox and address any failures before cutting a release.
4. Add a changelog entry and bump the patch version when dropping EOL Python support.
5. Ensure the README documents the versioning/support policy.
6. Create a NON master branch, commit the changes there only, and push that branch to the remote.

## Notes
- Keep version bumps to patch-level when removing EOL versions.
- Remove classifiers for dropped versions and add classifiers for newly supported versions.
