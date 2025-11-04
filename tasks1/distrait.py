import argparse
import json
import os
import sys
import datetime
import shutil
import textwrap
from pathlib import Path
from typing import List, Dict, Any, Optional

# Optional colors
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    HAS_COLORAMA = True
except Exception:
    HAS_COLORAMA = False
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        CYAN = ""
        MAGENTA = ""
        RESET = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""

# Data files (JSON) stored next to this script for portability
BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "distrait_tasks.json"
NOTES_FILE = BASE_DIR / "distrait_notes.json"


def load_json(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return []
            return json.loads(content)
    except Exception as e:
        print(f"Warning: Failed to load {path.name}: {e}. Starting fresh.")
        return []


def save_json(path: Path, data: List[Dict[str, Any]]):
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {path.name}: {e}")


def _next_id(items: List[Dict[str, Any]]) -> int:
    return max((it.get("id", 0) for it in items), default=0) + 1


def add_task(title: str, priority: int = 3, due: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    tasks = load_json(TASKS_FILE)
    task = {
        "id": _next_id(tasks),
        "title": title.strip(),
        "status": "pending",
        "priority": int(priority) if priority else 3,
        "tags": tags or [],
        "created_at": datetime.datetime.now().isoformat(),
        "due": due
    }
    tasks.append(task)
    save_json(TASKS_FILE, tasks)
    print(f"{Fore.GREEN}Added task{Fore.RESET}: ({task['id']}) {task['title']}")
    return task


def list_tasks(show_all: bool = True):
    tasks = load_json(TASKS_FILE)
    if not tasks:
        print("No tasks found.")
        return

    # sort by status, priority, due date
    def due_key(t):
        return t.get("due") or "~"

    tasks = sorted(tasks, key=lambda t: (t.get("status") == "complete", t.get("priority", 99), due_key(t)))

    print(f"{Style.BRIGHT}{Fore.CYAN}--- Tasks ---{Style.RESET_ALL}")
    for t in tasks:
        status = f"{Fore.GREEN}DONE{Fore.RESET}" if t.get("status") == "complete" else f"{Fore.YELLOW}PEND{Fore.RESET}"
        due = f" due:{t['due']}" if t.get("due") else ""
        tags = f" [{', '.join(t.get('tags', []))}]" if t.get('tags') else ""
        print(f"({t['id']}) {status} [p:{t.get('priority',3)}]{due} {t['title']}{tags}")


def complete_task(task_id: int):
    tasks = load_json(TASKS_FILE)
    for t in tasks:
        if t.get("id") == task_id:
            t["status"] = "complete"
            t["completed_at"] = datetime.datetime.now().isoformat()
            save_json(TASKS_FILE, tasks)
            print(f"{Fore.GREEN}Completed task{Fore.RESET}: ({task_id}) {t.get('title')}")
            return
    print(f"Task id {task_id} not found.")


def remove_task(task_id: int):
    tasks = load_json(TASKS_FILE)
    new = [t for t in tasks if t.get("id") != task_id]
    if len(new) == len(tasks):
        print(f"Task id {task_id} not found.")
        return
    save_json(TASKS_FILE, new)
    print(f"{Fore.RED}Removed task{Fore.RESET}: {task_id}")


def clear_tasks(confirm: bool = True):
    if confirm:
        ok = input("Really clear ALL tasks? Type 'yes' to confirm: ")
        if ok.strip().lower() != 'yes':
            print("Aborted.")
            return
    save_json(TASKS_FILE, [])
    print("All tasks cleared.")


def add_note(title: str, content: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    notes = load_json(NOTES_FILE)
    note = {
        "id": _next_id(notes),
        "title": title.strip(),
        "content": content.strip(),
        "tags": tags or [],
        "created_at": datetime.datetime.now().isoformat()
    }
    notes.append(note)
    save_json(NOTES_FILE, notes)
    print(f"{Fore.MAGENTA}Added note{Fore.RESET}: ({note['id']}) {note['title']}")
    return note


def list_notes():
    notes = load_json(NOTES_FILE)
    if not notes:
        print("No notes found.")
        return
    print(f"{Style.BRIGHT}{Fore.CYAN}--- Notes ---{Style.RESET_ALL}")
    for n in notes:
        tags = f" [{', '.join(n.get('tags', []))}]" if n.get('tags') else ""
        print(f"({n['id']}) {n['title']}{tags}\n  {textwrap.shorten(n['content'], width=120)}\n")


def search(query: str):
    q = query.lower()
    tasks = load_json(TASKS_FILE)
    notes = load_json(NOTES_FILE)
    t_matches = [t for t in tasks if q in t.get('title','').lower() or q in ' '.join(t.get('tags',[])).lower()]
    n_matches = [n for n in notes if q in n.get('title','').lower() or q in n.get('content','').lower() or q in ' '.join(n.get('tags',[])).lower()]

    if t_matches:
        print(f"{Fore.CYAN}Task matches:{Fore.RESET}")
        for t in t_matches:
            print(f"({t['id']}) {t['title']} [{', '.join(t.get('tags',[]))}]")
    else:
        print("No task matches.")

    if n_matches:
        print(f"\n{Fore.CYAN}Note matches:{Fore.RESET}")
        for n in n_matches:
            print(f"({n['id']}) {n['title']} - {textwrap.shorten(n['content'],80)}")
    else:
        print("No note matches.")


def export_all(path: Path):
    data = {
        'tasks': load_json(TASKS_FILE),
        'notes': load_json(NOTES_FILE)
    }
    save_json(path, [data])  # wrap so file is JSON array; keeps save_json signature
    print(f"Exported data to {path}")


def import_file(path: Path):
    if not path.exists():
        print(f"Import file {path} not found.")
        return
    try:
        with path.open('r', encoding='utf-8') as f:
            content = json.load(f)
            # allow either wrapped array or direct dict
            if isinstance(content, list) and content:
                content = content[0]
            tasks = content.get('tasks', [])
            notes = content.get('notes', [])
            save_json(TASKS_FILE, tasks)
            save_json(NOTES_FILE, notes)
            print(f"Imported tasks and notes from {path}")
    except Exception as e:
        print(f"Failed to import: {e}")


# Simple heuristic agents
def agent_suggest(task_count: int = 3):
    tasks = load_json(TASKS_FILE)
    pending = [t for t in tasks if t.get('status') != 'complete']
    # score by priority and proximity of due date
    def score(t):
        s = 100 - int(t.get('priority', 3)) * 10
        due = t.get('due')
        if due:
            try:
                dd = datetime.datetime.fromisoformat(due)
                days = (dd - datetime.datetime.now()).days
                s += max(0, 30 - days)
            except Exception:
                pass
        return s

    picked = sorted(pending, key=lambda t: -score(t))[:task_count]
    if not picked:
        print("No pending tasks to suggest.")
        return
    print(f"{Fore.CYAN}Suggested next tasks:{Fore.RESET}")
    for t in picked:
        print(f"({t['id']}) {t['title']} [p:{t.get('priority')}] due:{t.get('due')}")


def agent_summarize_notes(query: Optional[str] = None, max_chars: int = 800):
    notes = load_json(NOTES_FILE)
    if query:
        notes = [n for n in notes if query.lower() in (n.get('title','') + ' ' + n.get('content','')).lower()]
    if not notes:
        print("No notes to summarize.")
        return
    # naive summary: concatenate top N, shorten
    merged = "\n\n".join(n.get('title','') + "\n" + n.get('content','') for n in notes)
    print(f"{Style.BRIGHT}{Fore.MAGENTA}Notes summary:{Style.RESET_ALL}\n")
    print(textwrap.shorten(merged, width=max_chars, placeholder='...'))


def chat_interface():
    print(f"{Style.BRIGHT}{Fore.CYAN}Distrait Chat — type 'help' for commands, 'exit' to quit{Style.RESET_ALL}")
    while True:
        try:
            line = input('> ').strip()
        except EOFError:
            print('\nBye')
            return
        if not line:
            continue
        if line.lower() in ('exit','quit'):
            print('Bye')
            return
        if line.lower() == 'help':
            print("Commands: search <q>, suggest, summarize [q], tasks, notes, addtask <title>, addnote <title>|<content>")
            continue
        if line.startswith('search '):
            search(line[len('search '):])
            continue
        if line == 'suggest':
            agent_suggest()
            continue
        if line.startswith('summarize'):
            parts = line.split(' ',1)
            q = parts[1] if len(parts)>1 else None
            agent_summarize_notes(q)
            continue
        if line == 'tasks':
            list_tasks()
            continue
        if line == 'notes':
            list_notes()
            continue
        if line.startswith('addtask '):
            add_task(line[len('addtask '):])
            continue
        if line.startswith('addnote '):
            payload = line[len('addnote '):]
            if '|' in payload:
                title, content = payload.split('|',1)
                add_note(title.strip(), content.strip())
            else:
                print("Use: addnote title|content")
            continue
        print("Unknown chat command. Type 'help'.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Distrait — PKMS + Task manager + Chat (single-file)')
    sub = p.add_subparsers(dest='cmd')

    sp = sub.add_parser('add-task', help='Add a new task')
    sp.add_argument('title', nargs='+')
    sp.add_argument('--priority', '-p', type=int, default=3)
    sp.add_argument('--due', help='ISO date for due (YYYY-MM-DD or full ISO)')
    sp.add_argument('--tags', help='Comma separated tags')

    sub.add_parser('list-tasks', help='List tasks')

    spc = sub.add_parser('complete', help='Mark a task complete')
    spc.add_argument('id', type=int)

    spr = sub.add_parser('remove', help='Remove a task')
    spr.add_argument('id', type=int)

    sub.add_parser('clear-tasks', help='Clear all tasks')

    sn = sub.add_parser('add-note', help='Add a note')
    sn.add_argument('title')
    sn.add_argument('content')
    sn.add_argument('--tags')

    sub.add_parser('list-notes', help='List notes')

    ssearch = sub.add_parser('search', help='Search tasks and notes')
    ssearch.add_argument('query', nargs='+')

    ss = sub.add_parser('suggest', help='Agent: suggest next tasks')
    ss.add_argument('--n', type=int, default=3)

    ssum = sub.add_parser('summarize', help='Agent: summarize notes')
    ssum.add_argument('query', nargs='*')

    sub.add_parser('chat', help='Start the interactive chat interface')

    sex = sub.add_parser('export', help='Export tasks+notes to JSON file')
    sex.add_argument('path')

    six = sub.add_parser('import', help='Import tasks+notes from JSON file')
    six.add_argument('path')

    return p


def main(argv: Optional[List[str]] = None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == 'add-task':
        title = ' '.join(args.title)
        tags = [t.strip() for t in args.tags.split(',')] if getattr(args, 'tags', None) else []
        add_task(title, priority=args.priority, due=args.due, tags=tags)
    elif args.cmd == 'list-tasks':
        list_tasks()
    elif args.cmd == 'complete':
        complete_task(args.id)
    elif args.cmd == 'remove':
        remove_task(args.id)
    elif args.cmd == 'clear-tasks':
        clear_tasks()
    elif args.cmd == 'add-note':
        tags = [t.strip() for t in args.tags.split(',')] if getattr(args, 'tags', None) else []
        add_note(args.title, args.content, tags=tags)
    elif args.cmd == 'list-notes':
        list_notes()
    elif args.cmd == 'search':
        q = ' '.join(args.query)
        search(q)
    elif args.cmd == 'suggest':
        agent_suggest(getattr(args, 'n', 3))
    elif args.cmd == 'summarize':
        q = ' '.join(args.query) if getattr(args, 'query', None) else None
        agent_summarize_notes(q)
    elif args.cmd == 'chat' or args.cmd is None:
        # default to interactive chat if no command provided
        chat_interface()
    elif args.cmd == 'export':
        export_all(Path(args.path))
    elif args.cmd == 'import':
        import_file(Path(args.path))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
