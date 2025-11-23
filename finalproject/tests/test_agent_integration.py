from pkms import cli
from pkms.storage import StorageManager


def test_summarize_and_save(tmp_path):
    data_dir = str(tmp_path / "data")
    # create a longish note
    body = "".join(["This is a sentence. " for _ in range(50)])
    # add note
    cli.main(["--data-dir", data_dir, "add-note", "LongNote", body])
    sm = StorageManager(data_dir)
    notes = sm.list_notes()
    nid = notes[0].id
    # run summarization, save summary and accept first suggestion
    cli.main(["--data-dir", data_dir, "summarize-note", nid, "--save", "--accept"])
    notes2 = sm.list_notes()
    # expect at least one summary note with source agent
    agent_notes = [n for n in notes2 if n.source == "agent"]
    assert len(agent_notes) >= 1
    # expect at least one agent-created task
    tasks = sm.list_tasks()
    agent_tasks = [t for t in tasks if t.source == "agent"]
    assert len(agent_tasks) >= 1
