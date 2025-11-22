```markdown
# Quickstart: Names CLI

**Prerequisites**

- Python 3.14 or newer installed and available on `PATH`.
- The `uv` tool for project initialization (per project convention).

## Initialize the project

1. Initialize project with `uv` (project-specific tool):

```powershell
# Example (replace with actual uv invocation if different):
uv init
```

2. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install pytest
# Optional: install click if chosen
python -m pip install click
```

## Running the CLI

Add a name:

```powershell
python -m names_cli.cli add "Ada Lovelace"
```

List names:

```powershell
python -m names_cli.cli list
```

By default the data file is `./names.json` in the repository root. You can
override it with `--data-path <path>` if the CLI implements that option.

## Tests

Run unit and integration tests with `pytest`:

```powershell
pytest -q
```

## Notes

- The storage file is a UTF-8 encoded JSON array and is written atomically.
- Listing order is alphabetical (case-insensitive) using Unicode-aware
  comparison (`casefold`).

``` 
