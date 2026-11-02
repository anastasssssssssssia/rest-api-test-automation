import os
import sys
from pathlib import Path

import pytest

from helpers.user_helpers import UserValidator


def slow_tests_disabled() -> bool:
    return os.environ.get("RUN_SLOW") != "1"


@pytest.mark.skipif(sys.platform == "win32", reason="os.uname недоступен на Windows")
def test_os_uname_returns_system_name():
    assert os.uname().sysname != ""


@pytest.mark.skipif(slow_tests_disabled(), reason="RUN_SLOW не равен 1")
def test_all_ids_from_1_to_1000_are_valid():
    assert all(UserValidator.is_valid_id(user_id) for user_id in range(1, 1001))


def test_slow_test_runs_when_run_slow_is_one(pytester, monkeypatch):
    monkeypatch.setenv("RUN_SLOW", "1")
    pytester.makepyfile(test_slow=Path(__file__).read_text(encoding="utf-8"))
    result = pytester.runpytest("-k", "test_all_ids_from_1_to_1000_are_valid")
    result.assert_outcomes(passed=1)


@pytest.mark.skipif(False, reason="условие ложно")
def test_false_condition_does_not_skip():
    assert UserValidator.is_valid_id(1) is True


@pytest.mark.skipif(True, reason="условие истинно")
def test_true_condition_skips():
    assert UserValidator.is_valid_email("a@example.com") is True
