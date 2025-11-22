import os
from pathlib import Path

from names_cli import storage


def test_add_and_persist(tmp_path: Path):
    fp = tmp_path / "names.json"
    # Initially empty
    assert storage.read_names(fp) == []

    storage.add_name("Ada Lovelace", path=fp)
    assert "Ada Lovelace" in storage.read_names(fp)

    # Add another and verify persistence
    storage.add_name("Grace Hopper", path=fp)
    names = storage.read_names(fp)
    assert "Ada Lovelace" in names and "Grace Hopper" in names
