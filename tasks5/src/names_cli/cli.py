"""Simple CLI for names storage."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from names_cli import storage


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="names", description="Manage a local list of names")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add", help="Add a name")
    add_p.add_argument("name", nargs="+", help="Name to add (quote if contains spaces)")
    add_p.add_argument("--data-path", dest="data_path", help="Override data file path")

    list_p = sub.add_parser("list", help="List stored names")
    list_p.add_argument("--data-path", dest="data_path", help="Override data file path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    data_path = Path(args.data_path) if getattr(args, "data_path", None) else None

    if args.cmd == "add":
        # Join name parts if provided as multiple args
        raw_name = " ".join(args.name)
        try:
            storage.add_name(raw_name, path=data_path)
            print(f"Added: {raw_name}")
            return 0
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
    elif args.cmd == "list":
        names = storage.list_names(path=data_path)
        if not names:
            print("No names stored.")
            return 0
        for n in names:
            print(n)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
