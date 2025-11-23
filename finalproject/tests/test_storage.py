import tempfile
import os
from pkms.storage import StorageManager
from pkms.models import Note, Task


def test_notes_and_tasks_lifecycle(tmp_path):
    data_dir = str(tmp_path / "data")
    sm = StorageManager(data_dir)

    # Notes
    n = Note.create("T1", "Body here", tags=["x"]) 
    sm.add_note(n)
    listed = sm.list_notes()
    assert any(x.id == n.id for x in listed)

    sm.update_note(n.id, title="T1-updated")
    updated = [x for x in sm.list_notes() if x.id == n.id][0]
    assert updated.title == "T1-updated"

    sm.delete_note(n.id)
    assert all(x.id != n.id for x in sm.list_notes())

    # Tasks
    t = Task.create("Task1", description="do stuff")
    sm.add_task(t)
    assert any(x.id == t.id for x in sm.list_tasks())

    sm.mark_complete(t.id)
    done = [x for x in sm.list_tasks() if x.id == t.id][0]
    assert done.status == "done"

    sm.delete_task(t.id)
    assert all(x.id != t.id for x in sm.list_tasks())
