import json
import os
import tempfile
from typing import List, Optional, Dict, Any
from .models import Note, Task
from datetime import datetime, timezone


def default_data_dir() -> str:
    """Return a sensible cross-platform user data directory for the application."""
    home = os.path.expanduser("~")
    if os.name == "nt":
        appdata = os.getenv("APPDATA") or os.path.join(home, "AppData", "Roaming")
        return os.path.join(appdata, "pkms")
    else:
        return os.path.join(home, ".pkms")


class StorageError(Exception):
    pass


class StorageManager:
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or default_data_dir()
        os.makedirs(self.data_dir, exist_ok=True)
        self.notes_path = os.path.join(self.data_dir, "notes.json")
        self.tasks_path = os.path.join(self.data_dir, "tasks.json")

    def _read_file(self, path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            raise StorageError(f"Failed to read JSON from {path}: {exc}")

    def _atomic_write(self, path: str, data: List[Dict[str, Any]]):
        tmpfd, tmppath = tempfile.mkstemp(dir=self.data_dir)
        try:
            with os.fdopen(tmpfd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmppath, path)
        finally:
            if os.path.exists(tmppath):
                try:
                    os.remove(tmppath)
                except Exception:
                    pass

    # Notes operations
    def list_notes(self) -> List[Note]:
        raw = self._read_file(self.notes_path)
        return [Note.from_dict(d) for d in raw]

    def save_notes(self, notes: List[Note]):
        self._atomic_write(self.notes_path, [n.to_dict() for n in notes])

    def add_note(self, note: Note) -> Note:
        notes = self.list_notes()
        notes.append(note)
        self.save_notes(notes)
        return note

    def update_note(self, note_id: str, **changes) -> Note:
        notes = self.list_notes()
        found = False
        for n in notes:
            if n.id == note_id:
                for k, v in changes.items():
                    if hasattr(n, k):
                        setattr(n, k, v)
                n.updated_at = datetime.now(timezone.utc).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
                found = True
                updated = n
                break
        if not found:
            raise StorageError("Note not found")
        self.save_notes(notes)
        return updated

    def delete_note(self, note_id: str) -> None:
        notes = self.list_notes()
        notes = [n for n in notes if n.id != note_id]
        self.save_notes(notes)

    def search_notes(self, query: str, tag: Optional[str] = None) -> List[Note]:
        q = query.lower().strip()
        results = []
        for n in self.list_notes():
            hay = " ".join([n.title, n.body, " ".join(n.tags)]).lower()
            if q in hay:
                if tag:
                    if tag in n.tags:
                        results.append(n)
                else:
                    results.append(n)
        return results

    # Tasks operations
    def list_tasks(self) -> List[Task]:
        raw = self._read_file(self.tasks_path)
        return [Task.from_dict(d) for d in raw]

    def save_tasks(self, tasks: List[Task]):
        self._atomic_write(self.tasks_path, [t.to_dict() for t in tasks])

    def add_task(self, task: Task) -> Task:
        tasks = self.list_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
        return task

    def update_task(self, task_id: str, **changes) -> Task:
        tasks = self.list_tasks()
        found = False
        for t in tasks:
            if t.id == task_id:
                for k, v in changes.items():
                    if hasattr(t, k):
                        setattr(t, k, v)
                t.updated_at = datetime.now(timezone.utc).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
                found = True
                updated = t
                break
        if not found:
            raise StorageError("Task not found")
        self.save_tasks(tasks)
        return updated

    def delete_task(self, task_id: str) -> None:
        tasks = self.list_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        self.save_tasks(tasks)

    def mark_complete(self, task_id: str) -> Task:
        return self.update_task(task_id, status="done")

    # Backup / restore helpers
    def export(self, out_path: str) -> None:
        data = {"notes": [n.to_dict() for n in self.list_notes()], "tasks": [t.to_dict() for t in self.list_tasks()]}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_file(self, in_path: str, merge: bool = True) -> None:
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not merge:
            notes = [Note.from_dict(d) for d in data.get("notes", [])]
            tasks = [Task.from_dict(d) for d in data.get("tasks", [])]
        else:
            existing_notes = {n.id: n for n in self.list_notes()}
            existing_tasks = {t.id: t for t in self.list_tasks()}
            notes = list(existing_notes.values())
            for d in data.get("notes", []):
                n = Note.from_dict(d)
                if n.id not in existing_notes:
                    notes.append(n)
            tasks = list(existing_tasks.values())
            for d in data.get("tasks", []):
                t = Task.from_dict(d)
                if t.id not in existing_tasks:
                    tasks.append(t)
        self.save_notes(notes)
        self.save_tasks(tasks)

    def repair_from_backup(self, backup_path: str) -> None:
        # Overwrite current files with backup; simple recovery strategy
        with open(backup_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        notes = [Note.from_dict(d) for d in data.get("notes", [])]
        tasks = [Task.from_dict(d) for d in data.get("tasks", [])]
        self.save_notes(notes)
        self.save_tasks(tasks)
