from pathlib import Path
from typing import Union
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from django_debug_false_checker.__main__ import main

TEST_DIRECTORY = Path(__file__).parent / "fixtures"


def test_integration_no_args() -> None:
    with patch("sys.argv", ["django-debug-false-checker"]):
        with pytest.raises(SystemExit) as e:
            main()
    assert e.value.code == 0


@pytest.mark.parametrize(
    "file_path,expected",
    [
        ["settings", "Please change DEBUG to False"],
        ["not_real_settings_file", None],
        ["strange_formatting/settings", "Please change DEBUG to False"],
        ["actual_settings/settings", "Please change DEBUG to False"],
    ],
)
def test_integration(
    file_path: str, expected: Union[str, None], capsys: CaptureFixture
) -> None:
    file_path = str(TEST_DIRECTORY / f"{file_path}.py")
    with patch("sys.argv", ["django-debug-false-checker", file_path]):
        with pytest.raises(SystemExit) as e:
            main()
        expected_code = 0 if expected is None else -1
        assert e.value.code == expected_code
    out, err = capsys.readouterr()
    assert not out
    if expected is not None:
        assert expected in err
    else:
        assert not err
    assert err.count(file_path) <= 1
