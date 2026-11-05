import inspect

import pytest

from helpers.user_helpers import UserValidator


def test_is_valid_id_accepts_positive_id():
    assert UserValidator.is_valid_id(1) is True


def test_is_valid_id_rejects_zero():
    assert UserValidator.is_valid_id(0) is False


def test_is_valid_email_accepts_valid_address():
    assert UserValidator.is_valid_email("a@example.com") is True


def test_bool_is_not_valid_id():
    assert UserValidator.is_valid_id(True) is False


@pytest.mark.parametrize(
    "email",
    [
        "a@@example.com",
        "a@b@c.com",
        "a b@example.com",
        "a@exam ple.com",
        "invalid",
        "",
        "@example.com",
        "a@",
        "a@b",
        "a@.example.com",
        "a@example.com.",
    ],
)
def test_is_valid_email_rejects_invalid_addresses(email):
    assert UserValidator.is_valid_email(email) is False


def test_is_valid_id_is_called_on_class_without_instance():
    assert isinstance(inspect.getattr_static(UserValidator, "is_valid_id"), staticmethod)
    assert UserValidator.is_valid_id(3) is True
