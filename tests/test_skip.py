import pytest
import requests

from config.settings import TIMEOUT


@pytest.mark.skip(reason="сервис недоступен")
def test_payment_is_created(base_url):
    payment = {"userId": 1, "amount": 100, "currency": "RUB"}
    response = requests.post(f"{base_url}/payments", json=payment, timeout=TIMEOUT)
    assert response.status_code == 201


def test_skipped_test_makes_no_network_calls(pytester, monkeypatch):
    sent_requests = []
    monkeypatch.setattr(
        requests.Session,
        "request",
        lambda session, method, url, **kwargs: sent_requests.append((method, url)),
    )
    pytester.makepyfile(
        """
        import pytest
        import requests

        @pytest.mark.skip(reason="API недоступен")
        def test_unavailable_api():
            requests.get("https://unavailable-api.example/users", timeout=10)
        """
    )
    pytester.runpytest().assert_outcomes(skipped=1)
    assert sent_requests == []


@pytest.mark.skip(reason="экспериментальный поиск пользователей не готов")
def test_users_are_found_by_name(base_url):
    response = requests.get(f"{base_url}/users", params={"q": "Leanne"}, timeout=TIMEOUT)
    assert all("Leanne" in user["name"] for user in response.json())


def test_skip_and_regular_test_report_one_skipped_one_passed(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip(reason="сервис недоступен")
        def test_skipped():
            assert 2 * 2 == 4

        def test_regular():
            assert 2 * 2 == 4
        """
    )
    pytester.runpytest().assert_outcomes(passed=1, skipped=1)


def test_removing_skip_marker_makes_test_run(pytester):
    pytester.makepyfile(
        test_with_skip="""
        import pytest

        @pytest.mark.skip(reason="временно отключён")
        def test_sum():
            assert 2 + 2 == 4
        """,
        test_without_skip="""
        def test_sum():
            assert 2 + 2 == 4
        """,
    )
    pytester.runpytest("test_with_skip.py").assert_outcomes(skipped=1)
    pytester.runpytest("test_without_skip.py").assert_outcomes(passed=1)
