### Distrait — PKMS + Task Manager


Features
- Task manager: add-task, list-tasks, list-completed, complete, remove, clear-tasks, clear-completed
- Note manager: add-note, list-notes, search

Quick examples 
# show help (help includes short usage examples)
python distraitv2.py --help

# add a task (with priority, due date, and tags)
python distraitv2.py add-task "Write assignment report" -p 2 --due 2025-12-01 --tags school,urgent

# list all tasks
python distraitv2.py list-tasks

# mark a task complete (by id)
python distraitv2.py complete 3

# list completed tasks
python distraitv2.py list-completed

# remove a single task (by id)
python distraitv2.py remove 3

# remove a completed task by id
python distraitv2.py clear-completed 3

# clear all completed tasks (will prompt for confirmation)
python distraitv2.py clear-completed

# clear all tasks (will prompt for confirmation)
python distraitv2.py clear-tasks

# add a note (title and content)
python distraitv2.py add-note "Lecture notes" "Ideas about project architecture" --tags notes,proj

# list notes (shortened preview)
python distraitv2.py list-notes

# search tasks and notes for a keyword
python distraitv2.py search report
