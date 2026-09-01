---
name: dependency-update-and-version-bump
description: Use when asked to bump Python version support, GitHub Actions versions, or pre-commit hook versions in this repo (e.g. "bump the python support and github actions versions", "bump precommit versions", "remove unsupported python versions"). Checks each item against its upstream source of truth, applies the update, validates with the existing test/lint tooling, and bumps the package version and CHANGELOG per this repo's versioning policy when Python support changes.
---

# Dependency update and version bump

Covers three related, commonly-requested update types in a Python project that
uses GitHub Actions, pre-commit, and tox/pytest: Python version support,
GitHub Actions `uses:` versions, and pre-commit hook revisions. Handle
whichever subset the user asks for; all three follow the same shape: find
current upstream state, update every file that encodes the old value, then
validate.

This skill is deliberately harness-agnostic: every step is a plain shell
command or file edit, nothing here depends on a specific agent product. The
canonical copy lives at `.codex/skills/dependency-update-and-version-bump/`;
other harnesses should read a symlink into this directory (see "Making this
skill discoverable by other harnesses" below) rather than a duplicated copy.

## 1. Find every place a version is encoded

Before editing anything, grep the repo so you don't miss a file:

```
grep -rn "python-version\|requires-python\|Programming Language :: Python ::\|envlist\|py3[0-9]\|uses: .*@v\|rev: " \
  --include="*.yml" --include="*.yaml" --include="*.toml" --include="*.ini" --include="*.cfg" .
```

Typical hit locations in a project like this one:

- `.github/workflows/*.yml` — `uses: owner/action@vX` lines, and
  `python-version:` / matrix entries
- `pyproject.toml` — `requires-python`, `classifiers` Python version trove
  entries, `version`
- `tox.ini` — `envlist`
- `.pre-commit-config.yaml` — `rev:` per hook, `default_language_version`,
  and any hook `args` that embed a Python floor (e.g. pyupgrade's
  `--pyXY-plus`)
- `CHANGELOG.md` / `README.rst` — human-facing record of the change, if the
  project keeps one

## 2. Look up current upstream versions

Don't guess or rely on training-data knowledge of "latest" — versions move
constantly. Check the authoritative source for each item:

**Python support window** — search for the current Python release/EOL
schedule (e.g. endoflife.date/python, or the CPython devguide versions page).
Drop a version once it has reached EOL; add a version once it has a stable
(non-prerelease) release. Keep the floor (`requires-python`, tox `envlist`,
CI matrix) and the classifiers list in sync with each other.

**GitHub Actions** — query the public API directly, no auth required for
public repos:

```
curl -s "https://api.github.com/repos/<owner>/<action>/releases/latest" | grep -m1 '"tag_name"'
```

If that 404s (some actions don't mark a GitHub Release), fall back to tags:

```
curl -s "https://api.github.com/repos/<owner>/<action>/tags?per_page=5" | grep -m5 '"name"'
```

Some actions are intentionally pinned to a moving branch ref rather than a
version tag (e.g. `pypa/gh-action-pypi-publish@release/v1`) — leave those
alone, that's the maintainer-recommended usage, not a stale pin.

Watch for actions that share a version family and must stay paired (e.g.
`actions/upload-artifact` and `actions/download-artifact` both moved to a new
backend at v4 — don't downgrade one below the pairing floor even while
bumping both to their latest).

**pre-commit hooks** — same GitHub API lookup per hook `repo:` URL. A repo
that 301-redirects (check for `"message": "Moved Permanently"` in the API
response, or just a failed lookup) has likely moved owners — resolve the new
canonical URL and update the `repo:` field, not just the `rev:`, e.g.
`myint/autoflake` → `PyCQA/autoflake`, `sirosen/check-jsonschema` →
`python-jsonschema/check-jsonschema`. Cross-check anything you're unsure
about against the package's PyPI JSON API
(`https://pypi.org/pypi/<name>/json`, `.info.version`) since pre-commit
mirror tags usually track the underlying package version.

## 3. Present the proposed update list before editing

For each item: current value → proposed value, and one line on why (EOL
schedule, latest release, repo move). Apply only after the user confirms,
unless they've already framed the request as "just do it."

## 4. Apply the edits

- GitHub Actions: bump every `uses: owner/repo@vX` occurrence for that action
  across all workflow files — a single action is often referenced in more
  than one job/file.
- Python support: update `requires-python`, the classifiers block, tox
  `envlist`, the CI version matrix, `.pre-commit-config.yaml`'s
  `default_language_version.python`, and any `--pyXY-plus`-style tool args,
  together — a partial update leaves the config internally inconsistent.
- pre-commit: update `repo:` (if moved) and `rev:` per hook. If a formatter's
  `additional_dependencies` pins a version that should track another bumped
  hook (e.g. `blacken-docs`'s `additional_dependencies: [black==X]` tracking
  the `black` hook's own `rev:`), bump both together.

## 5. Validate

Run the project's existing tooling rather than inventing new checks:

```
tox -e py            # tests against the active interpreter
tox -e coverage       # if the project enforces a coverage floor
tox -e flake8          # or whatever the lint env is called
pre-commit run --all-files
```

`pre-commit run --all-files` will likely modify source files the first time
it runs against bumped hooks (newer pyupgrade rewriting syntax for the new
Python floor, a new black release reformatting under its updated style).
That's expected and correct — it's the bumped config doing its job. Re-run
the test suite after and keep the reformat; don't hand-revert it.

If a formatter warns about a Python-version mismatch (e.g. "Python X.Y
cannot parse code formatted for Python X.Y+1") because the interpreter
running the hook is older than the tool's autodetected target, treat it as
informational unless it actually fails — check the hook's exit code and
whether files still changed correctly.

## 6. Bump the package version and changelog, if the project has that policy

Check `README.rst` / `CONTRIBUTING` / an existing `CHANGELOG.md` pattern for
a stated versioning policy first — don't assume semver rules. A common
pattern: dropping support for an EOL Python version is a patch bump (it's a
support-matrix correction, not a feature or a breaking API change); adding
support for a new Python version alone doesn't require a bump on its own,
but is usually folded into the same patch release as the drop.

If the project keeps a `CHANGELOG.md`, add a dated entry above the previous
top entry, in whatever terse style existing entries already use (check the
last few entries for the format — don't introduce a new style).

## 7. Commit and push

Only commit/push directly to the default branch if that's this repo's
established convention (check recent `git log` — is history a series of
direct commits to main, or is everything merged through PRs?). If direct
pushes aren't the norm, use a branch instead. If the git remote is HTTPS and
push fails with a credential error in a sandboxed/headless environment, try
pushing the same ref over SSH (`git push git@github.com:<owner>/<repo>.git
HEAD:<branch>`) rather than reconfiguring the remote.

## Making this skill discoverable by other harnesses

Keep this file at `.codex/skills/dependency-update-and-version-bump/SKILL.md`
as the single canonical copy. Point other harnesses' skill directories at it
with a symlink instead of copying the content, so there's one file to keep
current:

```
ln -s ../.codex/skills .claude/skills   # Claude Code
```

Add further symlinks the same way for any other harness that looks for
skills in its own directory — the frontmatter (`name` + `description`) is
plain YAML and not tied to any one product.
