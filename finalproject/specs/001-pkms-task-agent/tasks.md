---
description: "Task list for Personal PKMS + Task Manager + AI Agents"
---

# Tasks: Personal PKMS + Task Manager + AI Agents

**Input**: `specs/001-pkms-task-agent/spec.md`
**Prerequisites**: `plan.md` (recommended), `spec.md` (required)

## Phase 1: Setup (Shared Infrastructure)

Purpose: Project initialization and basic structure

- [x] T001 Create project package `pkms/` with `__init__.py` and module placeholders (`pkms/models.py`, `pkms/storage.py`, `pkms/agent.py`, `pkms/cli.py`) — files: `pkms/__init__.py`, `pkms/models.py`, `pkms/storage.py`, `pkms/agent.py`, `pkms/cli.py`
- [x] T002 Initialize top-level runner and docs: add `pkms_cli.py` and `README.md` — files: `pkms_cli.py`, `README.md`
- [x] T003 [P] Create `tests/` directory and add initial test harness plus `requirements.txt` — files: `tests/`, `requirements.txt`, `tests/test_storage.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

Purpose: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Implement data models for `Note`, `Task`, `AgentResult` in `pkms/models.py` — file: `pkms/models.py`
- [x] T005 Implement JSON-backed storage manager with atomic writes and helpers in `pkms/storage.py` — file: `pkms/storage.py`
- [x] T006 [P] Implement simple agent helpers (summarize + suggestion heuristics) in `pkms/agent.py` — file: `pkms/agent.py`
- [x] T007 Implement CLI entrypoints and wiring in `pkms/cli.py` and top-level runner `pkms_cli.py` — files: `pkms/cli.py`, `pkms_cli.py`
- [x] T008 [P] Add automated tests and CI-ready test commands (`tests/test_storage.py`, `tests/test_cli.py`, `requirements.txt`) — files: `tests/test_storage.py`, `tests/test_cli.py`, `requirements.txt`
- [ ] T009 Configure basic linting/formatting and PR checks (add `.github/workflows/ci.yml` and lint config files) — files: `.github/workflows/ci.yml` (new), `.flake8` or `pyproject.toml` for formatters

Checkpoint: Foundation ready — user stories can now be implemented in parallel

---

## Phase 3: User Story 1 - Capture & Retrieve Notes (Priority: P1) 🎯 MVP

Goal: Create, tag, search and retrieve notes; persist to JSON

Independent Test: Create a note, search by keyword/tag, and retrieve it from `notes.json`.

### Tests (test-first)
- [x] T010 [P] [US1] Write unit tests for `Note` model and persistence in `tests/test_notes_model.py` — file: `tests/test_notes_model.py`
- [x] T011 [P] [US1] Write integration tests for note create/search/list flows in `tests/test_notes_integration.py` — file: `tests/test_notes_integration.py`

### Implementation
- [x] T012 [P] [US1] Create `Note` dataclass in `pkms/models.py` (fields id,title,body,tags,created_at,updated_at,source) — file: `pkms/models.py`
- [x] T013 [P] [US1] Implement `StorageManager` notes methods: `list_notes`, `add_note`, `update_note`, `delete_note`, `search_notes` in `pkms/storage.py` — file: `pkms/storage.py`
- [x] T014 [US1] Add CLI commands for notes: `add-note`, `list-notes`, `view-note`, `search-notes` in `pkms/cli.py` — file: `pkms/cli.py`
- [x] T015 [US1] Add JSON recovery/export/import helpers and document in `README.md` — files: `pkms/storage.py`, `README.md`
- [ ] T016 [US1] Run and pass `tests/test_notes_model.py` and `tests/test_notes_integration.py` in CI — CI file: `.github/workflows/ci.yml`

Checkpoint: US1 should be fully functional and independently testable

---

## Phase 4: User Story 2 - Task Management & Reminders (Priority: P1)

Goal: Create tasks, set due dates, toggle complete, list by status; persist to JSON

Independent Test: Create tasks, set due date, toggle complete flag, query active/overdue tasks.

### Tests (test-first)
- [x] T017 [P] [US2] Write unit tests for `Task` model and persistence in `tests/test_tasks_model.py` — file: `tests/test_tasks_model.py`
- [x] T018 [P] [US2] Write integration tests for task create/update/list flows in `tests/test_tasks_integration.py` — file: `tests/test_tasks_integration.py`

### Implementation
- [x] T019 [P] [US2] Create `Task` dataclass in `pkms/models.py` (fields id,title,description,due_date,status,created_at,updated_at,source) — file: `pkms/models.py`
- [x] T020 [P] [US2] Implement `StorageManager` task methods: `list_tasks`, `add_task`, `update_task`, `delete_task`, `mark_complete` in `pkms/storage.py` — file: `pkms/storage.py`
- [x] T021 [US2] Add CLI commands for tasks: `add-task`, `list-tasks`, `update-task`, `complete-task`, `delete-task` in `pkms/cli.py` — file: `pkms/cli.py`
- [ ] T022 [US2] Add overdue/due-soon filters and basic reminder logic (documented in `README.md`) — file: `pkms/cli.py`, `README.md`
- [ ] T023 [US2] Run and pass `tests/test_tasks_model.py` and `tests/test_tasks_integration.py` in CI — CI file: `.github/workflows/ci.yml`

Checkpoint: US2 should be independently testable and deployable

---

## Phase 5: User Story 3 - AI Summarization & Assistants (Priority: P2)

Goal: Provide an AI assistant action to summarize notes and propose task candidates.

Independent Test: Send a long note to summarize; verify summary note created and task suggestions returned/stored.

### Tests (test-first)
- [ ] T024 [P] [US3] Write unit tests for `agent.summarize_text` and `agent.suggest_tasks` in `tests/test_agent.py` — file: `tests/test_agent.py`
- [ ] T025 [P] [US3] Write integration test that triggers `summarize-note` CLI and verifies created summary and suggested tasks in `tests/test_agent_integration.py` — file: `tests/test_agent_integration.py`

### Implementation
- [x] T026 [P] [US3] Implement `summarize_text` and `suggest_tasks` heuristics in `pkms/agent.py` — file: `pkms/agent.py`
- [x] T027 [US3] Add `summarize-note` CLI command with `--accept` option to auto-create suggested tasks in `pkms/cli.py` — file: `pkms/cli.py`
- [x] T028 [US3] Add metadata attribution for agent-created tasks and notes (source=agent) in models/storage — files: `pkms/models.py`, `pkms/storage.py`
- [ ] T029 [US3] (Optional) Add integration with external AI providers configurable via `README.md` and `pkms/config.py` (if needed) — files: `pkms/config.py`, `README.md`

Checkpoint: US3 produces testable summaries and task suggestions

---

## Phase N: Polish & Cross-Cutting Concerns

Purpose: Improvements that affect multiple user stories

- [ ] T030 [P] Add CI workflow `.github/workflows/ci.yml` to run tests on Windows/macOS/Linux and linting — file: `.github/workflows/ci.yml`
- [ ] T031 [P] Add linting and formatting rules (e.g., `pyproject.toml` or `.flake8`) — files: `pyproject.toml` or `.flake8`
- [ ] T032 [P] Add documentation and quickstart in `specs/001-pkms-task-agent/quickstart.md` and expand `README.md` — files: `specs/001-pkms-task-agent/quickstart.md`, `README.md`
- [ ] T033 Implement accessibility, performance, and security checks described in `plan.md` as required — file references: `plan.md`

---

## Dependencies & Execution Order

- **Phase 1 (Setup)**: No dependencies — start immediately (T001..T003)
- **Phase 2 (Foundational)**: Depends on Setup (T004..T009) — BLOCKS user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion. Within each story, Tests (fail-first) → Models → Storage/Services → CLI → Integration tests

### User Story Dependencies
- **US1 (P1)**: Depends only on Foundational phase (T004..T009)
- **US2 (P1)**: Depends on Foundational phase; can run in parallel with US1 but may integrate with US1 storage
- **US3 (P2)**: Depends on Foundational and US1/US2 for persistence and CLI — lower priority

## Parallel Execution Examples

- Workstream A (Engineer): Implement `pkms/models.py` and unit tests for models (`T012`, `T019`, `T010`, `T017`)  — safe to run in parallel
- Workstream B (Engineer): Implement `pkms/storage.py` and integration tests (`T013`, `T020`, `T011`, `T018`) — independent file changes
- Workstream C (Engineer): Implement `pkms/cli.py` commands and CLI integration tests (`T014`, `T021`, `T025`) — once storage functions are available, CLI can be wired

## Implementation Strategy

- MVP First: Deliver Phase 1 + Phase 2 + Phase 3 (US1) to produce a usable MVP (notes capture, search, and persistence). Stop and validate.
- Incremental Delivery: After US1, add US2 tasks and tests; then add US3 agent features. Keep each story independently testable and deployable.
- Test-First: For every story, write tests that fail, implement minimal code to pass, then refactor.

---

## Counts & Summary

- Total tasks: 33
- Tasks by story: Setup:3, Foundational:6, US1:7, US2:7, US3:6, Polish:4
- Parallel opportunities: Setup & Foundational tasks with `[P]` markers; user stories can run in parallel after foundational completion.

Format validation: ALL tasks follow the checklist format (`- [ ] TXXX [P?] [US?] Description with file path`)
