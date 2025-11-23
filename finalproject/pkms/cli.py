"""Terminal CLI for lightweight PKMS.

Provides subcommands to manage notes and tasks and call the simple agent.
"""
from __future__ import annotations
import argparse
import sys
from .storage import StorageManager, StorageError
from .models import Note, Task
from .agent import summarize_text, suggest_tasks


def _print_note(n: Note):
    print(f"ID: {n.id}")
    print(f"Title: {n.title}")
    print(f"Tags: {', '.join(n.tags)}")
    print(f"Created: {n.created_at}  Updated: {n.updated_at}")
    print("---")
    print(n.body)
    print()


def _print_task(t: Task):
    print(f"ID: {t.id} | {t.title} | status={t.status} | due={t.due_date}")
    if t.description:
        print(f"  {t.description}")


def cmd_add_note(args):
    sm = StorageManager(args.data_dir)
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    note = Note.create(args.title, args.body, tags=tags)
    sm.add_note(note)
    print("Note added:")
    _print_note(note)


def cmd_list_notes(args):
    sm = StorageManager(args.data_dir)
    notes = sm.list_notes()
    for n in notes:
        print(f"- {n.id} | {n.title} | tags={','.join(n.tags)} | updated={n.updated_at}")


def cmd_view_note(args):
    sm = StorageManager(args.data_dir)
    for n in sm.list_notes():
        if n.id == args.id:
            _print_note(n)
            return
    print("Note not found", file=sys.stderr)
    sys.exit(2)


def cmd_search_notes(args):
    sm = StorageManager(args.data_dir)
    results = sm.search_notes(args.query, tag=args.tag)
    for n in results:
        print(f"- {n.id} | {n.title} | tags={','.join(n.tags)}")


def cmd_add_task(args):
    sm = StorageManager(args.data_dir)
    task = Task.create(title=args.title, description=args.description, due_date=args.due)
    sm.add_task(task)
    print("Task added:")
    _print_task(task)


def cmd_list_tasks(args):
    sm = StorageManager(args.data_dir)
    tasks = sm.list_tasks()
    if args.status:
        tasks = [t for t in tasks if t.status == args.status]
    for t in tasks:
        _print_task(t)


def cmd_complete_task(args):
    sm = StorageManager(args.data_dir)
    try:
        t = sm.mark_complete(args.id)
        print("Marked complete:")
        _print_task(t)
    except StorageError as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(2)


def cmd_summarize(args):
    sm = StorageManager(args.data_dir)
    note = None
    for n in sm.list_notes():
        if n.id == args.id:
            note = n
            break
    if not note:
        print("Note not found", file=sys.stderr)
        sys.exit(2)
    summary = summarize_text(note.body, max_sentences=args.sentences)
    suggestions = suggest_tasks(note.body, max_suggestions=args.max_suggestions)
    print("Summary:\n", summary)
    if getattr(args, "save", False):
        # Save the summary as a new note attributed to the agent
        summary_title = f"Summary: {note.title}" if note.title else "Summary"
        tags = ["summary", "agent"]
        if getattr(args, "notebook", None):
            tags.append(f"notebook:{args.notebook}")
        summary_note = Note.create(title=summary_title, body=summary, tags=tags, source="agent")
        sm.add_note(summary_note)
        print("Saved summary as note:")
        _print_note(summary_note)
    if suggestions:
        print("\nSuggested tasks:")
        for i, s in enumerate(suggestions, 1):
            print(f"{i}. {s['title']}")
        if args.accept:
            # accept the first suggestion by default when accept flag provided
            choice = 1
            sel = suggestions[choice - 1]
            task = Task.create(title=sel["title"], description=sel.get("excerpt", ""), source="agent")
            sm.add_task(task)
            print("Accepted suggestion -> task created:")
            _print_task(task)


def cmd_update_note(args):
    sm = StorageManager(args.data_dir)
    changes = {}
    if args.title:
        changes["title"] = args.title
    if args.body:
        changes["body"] = args.body
    if args.tags is not None:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        changes["tags"] = tags
    try:
        updated = sm.update_note(args.id, **changes)
        print("Updated note:")
        _print_note(updated)
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_delete_note(args):
    sm = StorageManager(args.data_dir)
    try:
        if not getattr(args, "yes", False):
            yn = input(f"Delete note {args.id}? This action cannot be undone. (y/N): ")
            if yn.strip().lower() not in ("y", "yes"):
                print("Aborted")
                return
        sm.delete_note(args.id)
        print("Note deleted")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_update_task(args):
    sm = StorageManager(args.data_dir)
    changes = {}
    if args.title:
        changes["title"] = args.title
    if args.description is not None:
        changes["description"] = args.description
    if args.due is not None:
        changes["due_date"] = args.due
    if args.status is not None:
        changes["status"] = args.status
    try:
        updated = sm.update_task(args.id, **changes)
        print("Updated task:")
        _print_task(updated)
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_delete_task(args):
    sm = StorageManager(args.data_dir)
    try:
        if not getattr(args, "yes", False):
            yn = input(f"Delete task {args.id}? This action cannot be undone. (y/N): ")
            if yn.strip().lower() not in ("y", "yes"):
                print("Aborted")
                return
        sm.delete_task(args.id)
        print("Task deleted")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_export(args):
    sm = StorageManager(args.data_dir)
    try:
        sm.export(args.path)
        print(f"Exported data to {args.path}")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_import(args):
    sm = StorageManager(args.data_dir)
    try:
        sm.import_file(args.path, merge=not args.replace)
        print(f"Imported data from {args.path}")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def cmd_repair(args):
    sm = StorageManager(args.data_dir)
    try:
        if not getattr(args, "yes", False):
            yn = input(f"Repair current data from backup {args.path}? This will overwrite current data. (y/N): ")
            if yn.strip().lower() not in ("y", "yes"):
                print("Aborted")
                return
        sm.repair_from_backup(args.path)
        print(f"Repaired data from backup {args.path}")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pkms", description="Simple PKMS CLI (notes + tasks + agent)")
    p.add_argument("--data-dir", help="Path to data directory (overrides default)")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add-note")
    a.add_argument("title")
    a.add_argument("body")
    a.add_argument("--tags", help="comma-separated tags")
    a.set_defaults(func=cmd_add_note)

    a = sub.add_parser("list-notes")
    a.set_defaults(func=cmd_list_notes)

    a = sub.add_parser("view-note")
    a.add_argument("id")
    a.set_defaults(func=cmd_view_note)

    a = sub.add_parser("search-notes")
    a.add_argument("query")
    a.add_argument("--tag")
    a.set_defaults(func=cmd_search_notes)

    a = sub.add_parser("add-task")
    a.add_argument("title")
    a.add_argument("--description", default="")
    a.add_argument("--due", default=None)
    a.set_defaults(func=cmd_add_task)

    a = sub.add_parser("list-tasks")
    a.add_argument("--status", choices=["todo", "in-progress", "done"])
    a.set_defaults(func=cmd_list_tasks)

    a = sub.add_parser("complete-task")
    a.add_argument("id")
    a.set_defaults(func=cmd_complete_task)

    a = sub.add_parser("summarize-note")
    a.add_argument("id")
    a.add_argument("--sentences", type=int, default=2)
    a.add_argument("--max-suggestions", type=int, default=3)
    a.add_argument("--accept", action="store_true", help="Auto-accept first suggestion and create a task")
    a.add_argument("--save", action="store_true", help="Save the generated summary as a new note (source=agent)")
    a.add_argument("--notebook", help="Name of notebook to tag the saved summary into (adds tag notebook:<name>)")
    a.set_defaults(func=cmd_summarize)

    a = sub.add_parser("update-note")
    a.add_argument("id")
    a.add_argument("--title")
    a.add_argument("--body")
    a.add_argument("--tags", help="comma-separated tags (set empty string to clear)")
    a.set_defaults(func=cmd_update_note)

    a = sub.add_parser("delete-note")
    a.add_argument("id")
    a.add_argument("--yes", action="store_true", help="Auto-confirm destructive action")
    a.set_defaults(func=cmd_delete_note)

    a = sub.add_parser("update-task")
    a.add_argument("id")
    a.add_argument("--title")
    a.add_argument("--description")
    a.add_argument("--due")
    a.add_argument("--status", choices=["todo", "in-progress", "done"])
    a.set_defaults(func=cmd_update_task)

    a = sub.add_parser("delete-task")
    a.add_argument("id")
    a.add_argument("--yes", action="store_true", help="Auto-confirm destructive action")
    a.set_defaults(func=cmd_delete_task)

    a = sub.add_parser("export")
    a.add_argument("path", help="Path to write exported JSON")
    a.set_defaults(func=cmd_export)

    a = sub.add_parser("import")
    a.add_argument("path", help="Path to read exported JSON")
    a.add_argument("--replace", action="store_true", help="Replace existing data instead of merge")
    a.set_defaults(func=cmd_import)

    a = sub.add_parser("repair")
    a.add_argument("path", help="Backup file to restore from")
    a.add_argument("--yes", action="store_true", help="Auto-confirm destructive action")
    a.set_defaults(func=cmd_repair)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        return 2
