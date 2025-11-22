# Names CLI

Small CLI to store and list names locally in a JSON file.

Usage:

```powershell
python -m names_cli.cli add "Ada Lovelace"
python -m names_cli.cli list
```

Default data file: `./names.json` in repository root. Use `--data-path` to
override.
