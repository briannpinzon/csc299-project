from pkms import cli
from pkms.storage import StorageManager


def test_task_search(tmp_path):
    data_dir = str(tmp_path / "data")
    # add tasks
    cli.main(["--data-dir", data_dir, "add-task", "Write report", "--description", "draft report"])
    cli.main(["--data-dir", data_dir, "add-task", "Call Bob", "--description", "discuss stats"])
    sm = StorageManager(data_dir)
    results = sm.search_tasks(query="report")
    assert any("report" in t.title.lower() or "report" in t.description.lower() for t in results)
    # CLI search
    cli.main(["--data-dir", data_dir, "search-tasks", "report"])
