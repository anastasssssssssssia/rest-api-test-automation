import pytest

from helpers.user_helpers import double


@pytest.mark.parametrize("value, expected", [(2, 4), (3, 6), (5, 10)])
def test_double_returns_twice_the_value(value, expected):
    assert double(value) == expected
