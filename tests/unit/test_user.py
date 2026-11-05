import pytest

from models.user import User


@pytest.fixture
def user() -> User:
    return User(id=1, first_name="Anna", last_name="Ivanova")


def test_full_name_joins_first_and_last_name(user):
    assert user.full_name == "Anna Ivanova"


def test_full_name_is_accessed_without_call(user):
    assert isinstance(User.full_name, property)
    assert not callable(user.full_name)
    assert user.full_name == "Anna Ivanova"


def test_full_name_reflects_first_name_change(user):
    user.first_name = "Maria"
    assert user.full_name == "Maria Ivanova"


def test_full_name_without_last_name_has_no_extra_space():
    user = User(id=1, first_name="Anna", last_name="")
    assert user.full_name == "Anna"


def test_full_name_is_read_only(user):
    with pytest.raises(AttributeError):
        user.full_name = "Other Name"
