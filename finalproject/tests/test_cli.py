import os
from pkms import cli
from pkms.storage import StorageManager


def test_cli_add_and_delete_note(tmp_path):
    data_dir = str(tmp_path / "data")
    # add note
    cli.main(["--data-dir", data_dir, "add-note", "T", "body", "--tags", "x"])
    sm = StorageManager(data_dir)
    notes = sm.list_notes()
    assert len(notes) == 1
    nid = notes[0].id
    # delete with --yes to bypass prompt
    cli.main(["--data-dir", data_dir, "delete-note", nid, "--yes"])
    assert len(sm.list_notes()) == 0


def test_cli_export_import(tmp_path):
    data_dir = str(tmp_path / "data1")
    out = str(tmp_path / "backup.json")
    cli.main(["--data-dir", data_dir, "add-note", "A", "b"])
    cli.main(["--data-dir", data_dir, "add-task", "T1"])
    cli.main(["--data-dir", data_dir, "export", out])
    assert os.path.exists(out)
    # import into new dir
    data_dir2 = str(tmp_path / "data2")
    cli.main(["--data-dir", data_dir2, "import", out])
    sm2 = StorageManager(data_dir2)
    assert len(sm2.list_notes()) == 1
    assert len(sm2.list_tasks()) == 1


def test_cli_update_task(tmp_path):
    data_dir = str(tmp_path / "data")
    cli.main(["--data-dir", data_dir, "add-task", "T1", "--description", "desc"])
    sm = StorageManager(data_dir)
    t = sm.list_tasks()[0]
    cli.main(["--data-dir", data_dir, "update-task", t.id, "--title", "NewT", "--status", "in-progress"])
    t2 = sm.list_tasks()[0]
    assert t2.title == "NewT"
    assert t2.status == "in-progress"
