from names_cli import cli


def test_cli_list_order(tmp_path, capsys):
    fp = tmp_path / "names.json"
    # Add multiple names
    rc = cli.main(["add", "bob", "--data-path", str(fp)])
    assert rc == 0
    rc = cli.main(["add", "Alice", "--data-path", str(fp)])
    assert rc == 0
    # clear add output
    capsys.readouterr()
    rc = cli.main(["list", "--data-path", str(fp)])
    assert rc == 0
    captured = capsys.readouterr()
    lines = [l.strip() for l in captured.out.splitlines() if l.strip()]
    assert lines == sorted(lines, key=lambda s: s.casefold())
