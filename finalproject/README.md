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
