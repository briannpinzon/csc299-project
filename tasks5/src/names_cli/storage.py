"""Storage layer for Names CLI.

Provides atomic read/write of a JSON array stored on disk and helpers for
adding and listing names with case-insensitive Unicode-aware sorting.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional


DEFAULT_FILENAME = "names.json"


def _default_path() -> Path:
    return Path(os.getcwd()) / DEFAULT_FILENAME


def read_names(path: Optional[Path | str] = None) -> List[str]:
    p = Path(path) if path else _default_path()
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [str(x) for x in data]
    except FileNotFoundError:
        return []
    except Exception:
        # On parse error, raise to surface the problem to caller
        raise
    return []


def write_names(names: List[str], path: Optional[Path | str] = None) -> None:
    p = Path(path) if path else _default_path()
    p_parent = p.parent
    p_parent.mkdir(parents=True, exist_ok=True)

    # Atomic write: write to temp file in same dir and replace
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(p_parent), encoding="utf-8") as tf:
        json.dump(names, tf, ensure_ascii=False, indent=2)
        temp_name = tf.name

    try:
        os.replace(temp_name, str(p))
    except Exception:
        # Attempt cleanup and re-raise
        try:
            os.remove(temp_name)
        except Exception:
            pass
        raise


def add_name(name: str, path: Optional[Path | str] = None) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must be non-empty")

    names = read_names(path)
    names.append(cleaned)
    write_names(names, path)


def list_names(path: Optional[Path | str] = None) -> List[str]:
    names = read_names(path)
    # Case-insensitive Unicode-aware sort
    return sorted(names, key=lambda s: s.casefold())
