import pytest

from helpers.user_helpers import UserValidator


@pytest.mark.xfail(reason="is_valid_email принимает адрес с двумя символами @")
def test_email_with_double_at_is_invalid():
    assert UserValidator.is_valid_email("a@@example.com") is False


@pytest.mark.xfail(reason="is_valid_id принимал True как id; дефект исправлен", strict=False)
def test_bool_is_not_valid_id():
    assert UserValidator.is_valid_id(True) is False


def test_strict_xfail_fails_on_unexpected_pass(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.xfail(reason="ожидаемый дефект", strict=True)
        def test_unexpected_pass():
            assert 3 * 2 == 6
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*XPASS(strict)*"])


@pytest.mark.xfail(raises=ValueError, reason="нечисловая строка не преобразуется в int")
def test_non_numeric_string_is_converted_to_int():
    assert int("not a number") == 0


def test_unexpected_exception_type_fails(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.xfail(raises=ValueError, reason="ожидается ValueError")
        def test_wrong_exception():
            raise TypeError("wrong type")
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*TypeError: wrong type*"])
