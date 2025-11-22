import sys
from types import SimpleNamespace

from names_cli import cli, storage


def test_cli_add_list(tmp_path, monkeypatch, capsys):
    fp = tmp_path / "names.json"

    # Run add
    rc = cli.main(["add", "Ada Lovelace", "--data-path", str(fp)])
    assert rc == 0

    # Run list and capture output
    rc = cli.main(["list", "--data-path", str(fp)])
    assert rc == 0

    captured = capsys.readouterr()
    assert "Ada Lovelace" in captured.out
