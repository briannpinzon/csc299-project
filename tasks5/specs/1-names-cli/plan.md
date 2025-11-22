```markdown
# Implementation Plan: Names CLI

**Branch**: `1-names-cli` | **Date**: 2025-11-21 | **Spec**: `specs/1-names-cli/spec.md`
**Input**: Feature specification from `/specs/1-names-cli/spec.md`

## Summary

Create a small, local CLI tool that stores a list of people names in a JSON
file. The CLI and storage layer will be separated: a `storage` module WILL
provide a small API to read/write the JSON array; the `cli` module WILL parse
arguments and call the storage API. The project will be initialized using the
`uv` tool and target Python >= 3.14.

## Technical Context

**Language/Version**: Python 3.14 (minimum)
**Project init**: `uv` (per user request)
**Primary Dependencies**: `click` or `argparse` for CLI (decided in implementation), `pytest` for testing
**Storage**: Local JSON file (`./names.json` in repo root by default)
**Testing**: `pytest` with unit tests for storage and integration tests for the CLI
**Target Platform**: Desktop developer environments (Windows, macOS, Linux)
**Performance Goals**: N/A (small local dataset; operations should be near-instant)
**Constraints**: Must keep CLI and storage logically separate; file I/O must be
atomic (write-temp + rename) with retry/backoff; listing must return
alphabetical order (case-insensitive, Unicode-aware)

### Unknowns / NEEDS_CLARIFICATION

- None remaining in the spec — clarifications were resolved earlier (file
  format: JSON array; concurrency: atomic write; storage path: repo root).

## Constitution Check

This plan MUST show how it satisfies the project's constitution principles.

- **Code Clarity & Simplicity**: Storage API will expose minimal, well-named
  functions (`read_names()`, `add_name(name)`, `list_names()`); tests will
  demonstrate behavior.
- **Code Quality & Maintainability**: Project will include linters (e.g.,
  `ruff`) and formatting (`black`). PRs will require peer review.
- **Testing Standards**: Unit tests for storage edge cases (empty name,
  unicode, duplicate handling, sorting) and integration tests that exercise
  the CLI end-to-end. CI must run tests and block merges until they pass.
- **User Experience Consistency**: `names add "Name"` and `names list` will
  be documented in README/quickstart with examples and expected outputs.
- **Observability & Release Discipline**: Not applicable for single-file local
  tool beyond clear changelog and semantic versioning for releases.

## Project Structure

```
specs/1-names-cli/
  ├── spec.md
  ├── plan.md
  ├── research.md
  ├── data-model.md
  ├── quickstart.md
  └── contracts/
      └── cli-contract.md
src/
  ├── names_cli/
  │   ├── __init__.py
  │   ├── storage.py   # storage API (read/write/sort)
  │   └── cli.py       # CLI entrypoint
  tests/
  ├── unit/
  └── integration/
pyproject.toml
README.md
names.json (default data file created on first add)
```

## Phase 0: Research

Tasks:
- Confirm Python 3.14 features needed (none required beyond standard lib for
  JSON/argparse; ensure `pathlib` and `tempfile` used for atomic writes).
- Best practices for atomic file replace on Windows (use os.replace or
  platform-safe rename semantics) and implement retry/backoff.
- Decide CLI library: `click` adds ergonomics; `argparse` avoids dependency.

Deliverable: `research.md` (this plan depends only on standard library; use
`click` optionally).

## Phase 1: Design

1. Create `data-model.md` describing the `Name` entity (string) and `Names
   Store` (JSON array), validation rules (non-empty, Unicode allowed), and
   sorting rules (case-insensitive, Unicode-aware casefolding).
2. Create `cli-contract.md` describing the `add` and `list` commands and
   their inputs/outputs.
3. Produce `quickstart.md` showing install and usage (including `uv` init
   steps), default storage path, and how to run tests.

## Phase 2: Tasks (high-level)

- T001 Setup project with `uv` and Python 3.14 in `pyproject.toml`.
- T002 Implement `storage.py`:
  - Read names (return Python list), write names atomically, add name,
    return sorted list (case-insensitive using `.casefold()`), validate input.
- T003 Implement `cli.py`:
  - Commands: `add`, `list`; `--data-path` optional flag to override default.
- T004 Add tests:
  - Unit: storage read/write, atomic write behavior (simulate rename failure), sorting, unicode support.
  - Integration: CLI add/list end-to-end using temp repo path.
- T005 Add docs: `README.md` and `specs/1-names-cli/quickstart.md` with usage examples and data file location.
- T006 Add CI workflow to run linters and tests on push/PR.

## Complexity Tracking

No constitution gates are violated. The design favors simplicity and local
storage; concurrency handled with atomic writes and documented limitations.

## Deliverables

- `specs/1-names-cli/plan.md` (this file)
- `specs/1-names-cli/research.md`
- `specs/1-names-cli/data-model.md`
- `specs/1-names-cli/quickstart.md`
- `specs/1-names-cli/contracts/cli-contract.md`

``` 
