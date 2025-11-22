---
description: "Task list for Names CLI feature"
---

# Tasks: Names CLI

**Input**: Design documents from `/specs/1-names-cli/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Project initialization)

- [x] T001 Initialize project with `uv` and create `pyproject.toml` (setup Python >=3.14) - `pyproject.toml`
- [x] T002 [P] Create source layout and package scaffolding - `src/names_cli/__init__.py`, `src/names_cli/cli.py`, `src/names_cli/storage.py`
- [x] T003 Initialize git and create .gitignore, add `names.json` to .gitignore if desired - `.gitignore`
- [x] T004 [P] Add development tools to `pyproject.toml`: `pytest`, `ruff`, `black` - `pyproject.toml`

## Phase 2: Foundational (Blocking prerequisites)

- [x] T005 Create `src/names_cli/storage.py` skeleton with functions: `read_names()`, `write_names(names)`, `add_name(name)`, `list_names()` - `src/names_cli/storage.py`
- [x] T006 [P] Implement atomic write helper (write-temp + os.replace) and retry/backoff utility - `src/names_cli/storage.py`
- [x] T007 [P] Add JSON file handling and default path support (`./names.json`) with optional `--data-path` override in storage API - `src/names_cli/storage.py`
- [x] T008 Add input validation (reject empty names) and Unicode trimming in storage layer - `src/names_cli/storage.py`
- [x] T009 [P] Add unit test harness and initial test config for pytest - `tests/unit/test_storage.py`, `pyproject.toml`

## Phase 3: User Story 1 - Add a name (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a name via CLI and persist it to `names.json`.

**Independent Test**: Run `python -m names_cli.cli add "Name"` then `python -m names_cli.cli list` to verify the name appears and persists.

- [x] T010 [US1] Implement `cli.add` command wiring to call `storage.add_name(name)` - `src/names_cli/cli.py`
- [x] T011 [US1] Unit test: `tests/unit/test_storage_add.py` — verify add_name writes JSON and persists across reads - `tests/unit/test_storage_add.py`
- [x] T012 [US1] Integration test: `tests/integration/test_cli_add_list.py` — end-to-end `add` then `list` against temp repo path - `tests/integration/test_cli_add_list.py`
- [x] T013 [US1] Update README and `specs/1-names-cli/quickstart.md` with `add` usage example - `README.md`, `specs/1-names-cli/quickstart.md`

## Phase 4: User Story 2 - List names (Priority: P1)

**Goal**: List stored names in alphabetical order (case-insensitive).

**Independent Test**: Add multiple names then run `names list`; assert output is sorted case-insensitively.

- [x] T014 [US2] Implement `storage.list_names()` to return sorted list using `casefold()` collation - `src/names_cli/storage.py`
- [x] T015 [US2] Implement `cli.list` command to print one name per line and friendly message on empty store - `src/names_cli/cli.py`
- [x] T016 [US2] Unit test: `tests/unit/test_storage_sort.py` — verify sorting and Unicode casefold behavior - `tests/unit/test_storage_sort.py`
- [x] T017 [US2] Integration test: `tests/integration/test_cli_list_order.py` — verify CLI prints names in the required order - `tests/integration/test_cli_list_order.py`

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T018 [P] Add linter and formatter configuration (`.ruff.toml`, `pyproject.toml` for `black`) - `.ruff.toml`, `pyproject.toml`
- [x] T019 [P] Add CI workflow to run linters and tests on push/PR - `.github/workflows/ci.yml`
- [x] T020 Add documentation: fill `README.md` with install, usage, and default data path details - `README.md`
- [x] T021 Create changelog template and initial entry noting v0.1.0 with doc and tests - `CHANGELOG.md`
- [ ] T022 [P] Add integration tests for concurrency scenario (atomic write semantics) - `tests/integration/test_concurrent_writes.py`

## Dependencies & Execution Order

- Foundation (T005-T009) MUST complete before user story work (T010+).
- User Stories US1 and US2 are independent after foundational tasks complete.
- Parallel opportunities: T002, T004, T006, T007, T009, T018, T019, T022 can run in parallel where staffing allows.

## Parallel execution examples

1. Run linters/formatters and unit tests in parallel:

```powershell
# Example: run in separate terminals or CI jobs
ruff src tests || true
black --check src tests || true
pytest tests/unit -q
```

## Implementation Strategy

- MVP First: Implement foundation + US1 (add) → validate persistence and tests → then implement US2 (list) and sorting.
- Incremental Delivery: ensure each story has unit + integration tests before merging.

## Task counts & summary

- Total tasks: 22
- Tasks per story:
  - Setup/Foundation: 9
  - US1 (Add): 4
  - US2 (List): 4
  - Polish & Cross-cutting: 5

## Suggested MVP

- Complete Phase 1 + Phase 2 + Phase 3 (US1) to deliver a working `add` and persistence feature.
