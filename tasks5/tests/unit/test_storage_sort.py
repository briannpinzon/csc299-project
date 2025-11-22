from names_cli import storage


def test_sorting_case_insensitive(tmp_path):
    fp = tmp_path / "names.json"
    names = ["bob", "Alice", "álvaro"]
    storage.write_names(names, path=fp)
    sorted_names = storage.list_names(path=fp)
    # casefold-based sorting should place 'Alice' before 'bob'
    assert sorted_names[0].casefold() <= sorted_names[1].casefold()
    assert "Alice" in sorted_names
