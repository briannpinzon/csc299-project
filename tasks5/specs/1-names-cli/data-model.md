```markdown
# Data Model: Names CLI

**Feature**: Names CLI
**Date**: 2025-11-21

## Entities

- Name
  - Type: string
  - Description: Display form of a person's name. Unicode allowed.
  - Validation: Non-empty, trimmed of leading/trailing whitespace.

- Names Store
  - Type: JSON array of `Name` strings persisted to `./names.json` by default.
  - Behavior: Append on add (then write full array atomically); `list` returns
    items sorted alphabetically (case-insensitive) using `casefold()`.

## Validation Rules

- `add_name(name)`: Reject if `name.strip()` is empty; otherwise accept.
- `read_names()`: If file not present, return empty list.

## State Transitions

- On `add`: read current array → append validated name → write atomically → return success.

``` 
