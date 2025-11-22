```markdown
# CLI Contract: Names CLI

**Command**: `names add <name>`
- Input: single positional string `name` (may contain spaces; should be quoted)
- Output: exit code 0 on success; prints confirmation message to stdout
- Failure: exit code != 0 and an actionable error message on stderr when input invalid

**Command**: `names list`
- Input: none
- Output: prints stored names to stdout, one per line, in alphabetical order (case-insensitive). If no names stored, prints a friendly message (e.g., "No names stored."). Exit code 0.

**Flags / options (optional)**
- `--data-path <path>`: override default storage path (`./names.json`). If provided,
  CLI uses this path for read/write operations.

**Format guarantees**
- Data file: UTF-8 encoded JSON array of strings.
- Sorting: casefold-based Unicode-aware, documented in plan.

``` 
