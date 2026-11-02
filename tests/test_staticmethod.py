import inspect

from helpers.user_helpers import UserValidator


def test_is_valid_id_accepts_positive_id():
    assert UserValidator.is_valid_id(1) is True


def test_is_valid_id_rejects_zero():
    assert UserValidator.is_valid_id(0) is False


def test_is_valid_email_accepts_valid_address():
    assert UserValidator.is_valid_email("a@example.com") is True


def test_is_valid_email_rejects_string_without_at():
    assert UserValidator.is_valid_email("invalid") is False


def test_is_valid_id_is_called_on_class_without_instance():
    assert isinstance(inspect.getattr_static(UserValidator, "is_valid_id"), staticmethod)
    assert UserValidator.is_valid_id(3) is True
