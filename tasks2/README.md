Distrait — PKMS + Task Manager (single-file)



> Compact Personal Knowledge Management + Task Manager implemented in one Python script.



Features

\- JSON-backed storage: `distrait\_tasks.json`, `distrait\_notes.json` (next to the script)

\- Task manager: add-task, list-tasks, complete, remove, clear-tasks

\- Note manager: add-note, list-notes, search

\- Export / Import full state as JSON

\- Optional colored output if `colorama` is installed; otherwise graceful fallback



Quick examples (PowerShell)



```powershell

\# show help

python .\\distrait.py --help



\# add a task

python .\\distrait.py add-task "Write assignment report" -p 2 --due 2025-12-01 --tags school,urgent



\# list tasks

python .\\distrait.py list-tasks



\# start interactive chat (smart search, summaries, quick add)

python .\\distrait.py chat

```



Storage

\- `distrait\_tasks.json` and `distrait\_notes.json` live next to `distrait.py`. They're plain JSON files you can edit or back up.



Next steps

\- Add more tests (integration)

\- Add optional LLM integration for richer agent behavior





Distrait is a simple program that helps you track important tasks in a JSON file 







\\## Commands 







\\# \\\*\\\*add\\\*\\\*







Adds a new task to a JSON file



i.e. \\\*python add "desired task here"







\\# List







Lists all tasks



i.e. \\\*python list\\\*







\\# Search







Searches for a task



i.e. \\\*python search keyword\\\*





