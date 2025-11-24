PKMS - Minimal Personal Knowledge & Task Manager
----------------------------------------------

This is a small terminal-first Python app that stores notes and tasks in JSON files and includes a simple AI agent stub for summarization and task suggestion.

Requirements
- Python 3.10+

Quick start (Windows PowerShell / macOS / Linux)

1) Run the CLI directly:

```powershell
python pkms_cli.py add-note "Meeting" "Agenda: discuss roadmap" --tags "work,meeting"
python pkms_cli.py list-notes
python pkms_cli.py add-task "Finish report" --description "Finalize figures" --due "2025-11-25"
python pkms_cli.py list-tasks
python pkms_cli.py search-tasks "report" --status todo

Summarization examples:
```powershell
python pkms_cli.py summarize-note <note-id> --save --notebook "meetings"
python pkms_cli.py summarize-note <note-id> --save --accept --notebook "meetings"
```
```

2) Data files are stored in the default user data directory:
- Windows: `%APPDATA%\pkms\notes.json` and `%APPDATA%\pkms\tasks.json`
- macOS / Linux: `~/.pkms/notes.json` and `~/.pkms/tasks.json`

Notes
- The summarizer and suggestion engine are intentionally simple (no external AI). Replace `pkms.agent` with integrations to external providers if desired.

Running tests
- Tests are under `tests/` and can be run with `pytest` (optional). See `requirements.txt` for test dependencies.

Detailed usage & developer reference
-----------------------------------

This section lists the CLI commands and primary library functions you may use, why they exist, and short examples.

CLI Commands (what to use from terminal)
- `add-note <title> <body> [--tags <tags>]`
	- Purpose: Create a new note. `--tags` accepts a comma-separated list.
	- Example: `python pkms_cli.py add-note "Meeting" "Agenda: discuss roadmap" --tags "work,meeting"`

- `list-notes`
	- Purpose: Show all saved notes (id, title, tags, updated timestamp).
	- Example: `python pkms_cli.py list-notes`

- `view-note <id>`
	- Purpose: Print full note contents for a specific note id.
	- Example: `python pkms_cli.py view-note 123e4567`

- `search-notes <query> [--tag <tag>]`
	- Purpose: Search note titles/bodies for `query`; optionally filter by a tag.
	- Example: `python pkms_cli.py search-notes "roadmap" --tag work`

- `add-task <title> [--description <description>] [--due <due>]`
	- Purpose: Create a task with optional description and due date (ISO string or free text).
	- Example: `python pkms_cli.py add-task "Finish report" --description "Finalize figures" --due "2025-11-25"`

- `list-tasks [--status todo|in-progress|done]`
	- Purpose: List tasks; filterable by status.
	- Example: `python pkms_cli.py list-tasks --status todo`

- `search-tasks [query] [--status <status>]`
	- Purpose: Search tasks by title/description; can also filter by status.
	- Example: `python pkms_cli.py search-tasks report --status todo`

- `complete-task <id>`
	- Purpose: Mark a task as complete (status changes to `done`).
	- Example: `python pkms_cli.py complete-task 123e4567`

- `update-task <id> [--title] [--description] [--due] [--status]`
	- Purpose: Update fields of a task.
	- Example: `python pkms_cli.py update-task 123e4567 --status in-progress`

- `delete-task <id> [--yes]`
	- Purpose: Remove a task. `--yes` bypasses interactive confirmation.
	- Example: `python pkms_cli.py delete-task 123e4567 --yes`

- `update-note <id> [--title] [--body] [--tags]`
	- Purpose: Update a note's fields. Passing `--tags ""` clears tags.
	- Example: `python pkms_cli.py update-note 123e4567 --title "New title"`

- `delete-note <id> [--yes]`
	- Purpose: Remove a note. `--yes` bypasses interactive confirmation.
	- Example: `python pkms_cli.py delete-note 123e4567 --yes`

- `summarize-note <id> [--sentences N] [--max-suggestions N] [--save] [--accept] [--notebook <name>]`
	- Purpose: Produce a short summary of a note (agent stub). Optionally save the summary as a new note (`--save`), auto-create a task from the first suggestion (`--accept`), and tag saved summaries into a notebook tag via `--notebook`.
	- Example: `python pkms_cli.py summarize-note 123e4567 --sentences 3 --save --notebook "meetings"`

- `export <path>`
	- Purpose: Export current notes+tasks JSON to the provided path (backup or transfer).
	- Example: `python pkms_cli.py export backup.json`

- `import <path> [--replace]`
	- Purpose: Import notes+tasks JSON. By default this merges; `--replace` overwrites existing data.
	- Example: `python pkms_cli.py import backup.json --replace`

- `repair <path> [--yes]`
	- Purpose: Restore data from a backup file into the active data directory (destructive). Confirm with `--yes` to skip the prompt.
	- Example: `python pkms_cli.py repair backup.json --yes`

Developer API (for importing the package from Python)
- `pkms.storage.StorageManager(data_dir=None)`
	- Key methods:
		- `list_notes()` -> [Note]
		- `add_note(note: Note)` -> None
		- `update_note(id, **changes)` -> Note
		- `delete_note(id)` -> None
		- `search_notes(query, tag=None)` -> [Note]
		- `list_tasks()` -> [Task]
		- `add_task(task: Task)` -> None
		- `update_task(id, **changes)` -> Task
		- `delete_task(id)` -> None
		- `mark_complete(id)` -> Task
		- `search_tasks(query=None, status=None)` -> [Task]
		- `export(path)` -> None
		- `import_file(path, merge=True)` -> None
		- `repair_from_backup(path)` -> None
	- Purpose: Central JSON-backed storage manager with atomic writes and utilities for export/import/repair.
	- Usage example (Python):
		```python
		from pkms.storage import StorageManager
		sm = StorageManager()
		notes = sm.list_notes()
		sm.add_note(Note.create("Title","Body", tags=["x"]))
		```

- `pkms.agent` (simple agent helpers)
	- `summarize_text(text: str, max_sentences: int = 2) -> str`
		- Purpose: Return a concise summary of text. Replaceable for real AI integration.
		- Example: `summarize_text(note.body, max_sentences=3)`
	- `suggest_tasks(text: str, max_suggestions: int = 5) -> list[dict]`
		- Purpose: Heuristic-based task suggestions derived from text; returns items like `{"title":..., "excerpt":...}`.
		- Example: `suggest_tasks(note.body)`

- `pkms.models` dataclasses
	- `Note.create(title, body, tags=[], source=None)`
	- `Task.create(title, description='', due_date=None, source=None)`
	- Purpose: Constructors and serialization helpers used by storage and CLI.

Data files
- Default data directory:
	- Windows: `%APPDATA%\\pkms\\notes.json` and `%APPDATA%\\pkms\\tasks.json`
	- macOS / Linux: `~/.pkms/notes.json` and `~/.pkms/tasks.json`

Running tests
- Run the full test suite using `pytest` from the repository root:

```powershell
pytest -q
'''