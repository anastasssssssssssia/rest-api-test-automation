import requests

from config.settings import TIMEOUT


def test_user_data_contains_expected_values(user_data):
    assert user_data["id"] == 1
    assert user_data["name"] == "Anna"
    assert user_data["email"] == "anna@example.com"


def test_user_data_can_be_modified_within_test(user_data):
    user_data["name"] = "Changed"
    assert user_data["name"] == "Changed"
    assert user_data["email"] == "anna@example.com"


def test_user_data_is_not_affected_by_other_tests(user_data):
    assert user_data["name"] == "Anna"
    assert user_data["id"] == 1
    assert user_data["email"] == "anna@example.com"


def test_base_url_get_user_returns_user_one(base_url):
    response = requests.get(f"{base_url}/users/1", timeout=TIMEOUT)
    assert response.status_code == 200
    user = response.json()
    assert type(user["id"]) is int
    assert user["id"] == 1
    assert "username" in user


def test_yield_fixture_clears_items_after_test(temp_items, cleanup_counter):
    assert temp_items == ["temp"]
    assert cleanup_counter["cleanups"] == 0


def test_module_fixture_is_set_up_once(module_setup_state):
    assert module_setup_state["setups"] == 1


def test_module_fixture_is_reused_within_module(module_setup_state):
    assert module_setup_state["setups"] == 1
