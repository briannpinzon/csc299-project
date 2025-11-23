```markdown
# Implementation Plan: Personal PKMS + Task Manager + AI Agents

**Branch**: `001-pkms-task-agent` | **Date**: 2025-11-23 | **Spec**: `spec.md`

## Summary

Deliver a terminal-first Python 3.10+ application that stores notes and tasks in JSON and provides a simple AI agent for summarization and task suggestion. Start with core persistence, CLI, and tests; then add CI and optional provider integrations.

## Technical Context

- **Language/Version**: Python 3.10+
- **Primary Dependencies**: None mandatory; `pytest` for tests
- **Storage**: Local JSON files (`notes.json`, `tasks.json`) under user data dir
- **Testing**: `pytest`
- **Target Platform**: Windows, macOS, Linux (CLI)

## Constitution Check

Passes the project constitution: Test-first, code-quality, and UX consistency followed. Tests added and run locally.

## Project Structure

```
specs/001-pkms-task-agent/
  - spec.md
  - tasks.md
  - checklists/
  - plan.md

pkms/
  - __init__.py
  - models.py
  - storage.py
  - agent.py
  - cli.py

tests/
  - test_storage.py
  - test_cli.py
  - test_agent.py
  - test_agent_integration.py

pkms_cli.py
README.md
requirements.txt
```

## CI / Release

- Add `.github/workflows/ci.yml` to run tests on pushes and PRs across OS matrix (already scaffolded in repo).

## Plan Steps

1. Finish remaining polish items (CI linting, README expansion).
2. Optionally integrate external AI providers behind a small adapter interface.
3. Create release candidate and document upgrade/migration steps for external storage.

## Acceptance

- All unit and integration tests pass across supported platforms in CI.
- CLI provides commands for notes/tasks and agent actions; summaries can be saved and tasks created from suggestions.

``` 