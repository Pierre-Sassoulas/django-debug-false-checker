"""Check that django DEBUG = True in settings.py. Used by pre-commit."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Callable

from django_debug_false_checker._ast_check import _ast_check

logger = logging.getLogger(__name__)


def main(
    argv: list[str] | None = None,
    check_function: Callable[[str, str], bool] = _ast_check,
) -> None:
    args = _parse_args(argv)
    offending_files: set[str] = set()
    for file_name in args.filenames:
        if "settings.py" not in file_name:
            continue
        try:
            with open(file_name, encoding="utf8") as f:
                file_content = f.read()
        except UnicodeDecodeError as e:  # pragma: no cover
            logger.exception(e)
            continue
        if not check_function(file_name, file_content):
            offending_files.add(file_name)
    _display_result(offending_files)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to modify",
    )
    args = parser.parse_args(argv)
    return args


def _display_result(offending_files):
    if offending_files:
        print(
            f"Please change DEBUG to False in '{', '.join(offending_files)}',",
            file=sys.stderr,
        )
        sys.exit(-1)
    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
