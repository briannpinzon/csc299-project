```markdown
# Research: Names CLI

**Feature**: Names CLI (`specs/1-names-cli/spec.md`)
**Date**: 2025-11-21

## Decisions

- Decision: Use JSON array file format
  - Rationale: Simple, human-readable, extensible. Matches user choice.
  - Alternatives considered: newline-delimited text (simpler but less
    extensible), SQLite (overkill for small local dataset).

- Decision: Atomic write strategy (temp file + rename) with retry/backoff
  - Rationale: Protects against file corruption in concurrent writes without
    adding DB dependencies. Use `os.replace` (atomic on POSIX and Windows)
    where available; implement retry on failure.

- Decision: Default storage location is `./names.json` in the repository root
  - Rationale: Matches user selection for repo-local storage and is
    predictable for developers.

- Decision: Python CLI library: `argparse` (standard lib) by default; allow
  `click` as optional dependency if ergonomics desired.
  - Rationale: Minimizes dependencies; `argparse` is sufficient for two
    commands. If richer CLI UX needed later, adopt `click`.

## Implementation Notes

- Windows considerations: `os.replace` provides atomic replacement on
  Windows and POSIX; if not, use `pathlib` with `replace()` and document
  behavior.
- Sorting: use `str.casefold()` for case-insensitive Unicode-aware ordering.

``` 
