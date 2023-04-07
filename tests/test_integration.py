from pathlib import Path
from typing import Callable, Union
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from django_debug_false_checker.__main__ import main
from django_debug_false_checker._ast_check import _ast_check

TEST_DIRECTORY = Path(__file__).parent / "fixtures"


def test_integration_no_args() -> None:
    with patch("sys.argv", ["django-debug-false-checker"]):
        with pytest.raises(SystemExit) as e:
            main()
    assert e.value.code == 0


@pytest.mark.parametrize("file_path", [str(p) for p in TEST_DIRECTORY.rglob("*.py")])
@pytest.mark.parametrize("check_function", [_ast_check])
def test_integration(
    file_path: str, check_function: Callable[[str, str], bool], capsys: CaptureFixture
) -> None:
    if any(x in file_path for x in ["not_real_settings_file.py"]):
        expected = None
    else:
        expected = "Please change DEBUG to False"
    _test_file_path(file_path, expected, check_function, capsys)


def _test_file_path(
    file_path: str,
    expected: Union[str, None],
    check_function: Callable[[str, str], bool],
    capsys: CaptureFixture,
):
    with patch("sys.argv", ["django-debug-false-checker", file_path]):
        with pytest.raises(SystemExit) as e:
            main(check_function=check_function)
        expected_code = 0 if expected is None else -1
        assert e.value.code == expected_code
    out, err = capsys.readouterr()
    assert not out
    if expected is not None:
        assert expected in err, (
            f"Didn't get the expected {expected} when "
            f"checking {file_path} with {check_function}"
        )
    else:
        assert (
            not err
        ), f"Got a false positive when checking {file_path} with {check_function}"
    assert err.count(file_path) <= 1
