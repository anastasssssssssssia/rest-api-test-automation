import pytest
import requests

from config.settings import TIMEOUT


def test_get_user_returns_200(api_client):
    response = api_client.get_user(1)
    assert response.status_code == 200


def test_get_user_returns_requested_id(api_client):
    response = api_client.get_user(1)
    assert response.json()["id"] == 1


def test_get_user_has_required_fields(api_client):
    user = api_client.get_user(1).json()
    for field in ("id", "name", "username", "email"):
        assert field in user


def test_get_user_field_types(api_client):
    user = api_client.get_user(1).json()
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["username"], str)
    assert isinstance(user["email"], str)


def test_get_user_address_contains_city(api_client):
    user = api_client.get_user(1).json()
    assert isinstance(user["address"], dict)
    assert "city" in user["address"]


def test_get_users_returns_non_empty_list(api_client):
    users = api_client.get_users().json()
    assert isinstance(users, list)
    assert len(users) > 0


def test_get_users_each_has_id_and_email(api_client):
    users = api_client.get_users().json()
    for user in users:
        assert "id" in user
        assert "email" in user


def test_get_nonexistent_user_returns_404(api_client):
    response = api_client.get_user(999999)
    assert response.status_code == 404


def test_base_url_get_user_1_returns_200(base_url):
    response = requests.get(f"{base_url}/users/1", timeout=TIMEOUT)
    assert response.status_code == 200


def test_base_url_get_user_2_returns_200(base_url):
    response = requests.get(f"{base_url}/users/2", timeout=TIMEOUT)
    assert response.status_code == 200


def test_base_url_get_users_returns_list(base_url):
    response = requests.get(f"{base_url}/users", timeout=TIMEOUT)
    assert isinstance(response.json(), list)


def test_user_data_id_is_one(user_data):
    assert user_data["id"] == 1


def test_user_data_name_is_anna(user_data):
    assert user_data["name"] == "Anna"


def test_user_data_email_is_str(user_data):
    assert isinstance(user_data["email"], str)


def test_user_data_age_is_int(user_data):
    assert isinstance(user_data["age"], int)


def test_user_data_active_is_bool(user_data):
    assert isinstance(user_data["active"], bool)


def test_user_data_has_required_keys(user_data):
    for key in ("id", "name", "email", "age", "active"):
        assert key in user_data


def test_user_data_age_is_greater_than_18(user_data):
    assert user_data["age"] > 18


def test_user_response_status_code_is_200(user_response):
    assert user_response.status_code == 200


def test_user_response_body_is_valid_json(user_response):
    try:
        user_response.json()
    except requests.exceptions.JSONDecodeError:
        pytest.fail(f"Ответ не является JSON: {user_response.text!r}")


def test_user_response_json_is_dict(user_response):
    assert isinstance(user_response.json(), dict)


def test_user_response_has_id(user_response):
    assert "id" in user_response.json()


def test_user_response_has_name(user_response):
    assert "name" in user_response.json()


def test_user_response_has_email(user_response):
    assert "email" in user_response.json()


def test_user_json_id_is_two(user_json):
    assert user_json["id"] == 2


def test_user_json_name_is_str(user_json):
    assert isinstance(user_json["name"], str)


def test_user_json_name_is_not_empty(user_json):
    assert user_json["name"] != ""


def test_user_json_has_email(user_json):
    assert "email" in user_json


def test_user_json_username_is_str(user_json):
    assert isinstance(user_json["username"], str)


def test_user_json_address_is_dict(user_json):
    assert isinstance(user_json["address"], dict)


def test_user_json_city_is_non_empty_string(user_json):
    city = user_json["address"]["city"]
    assert isinstance(city, str)
    assert city != ""


def test_users_response_status_code_is_200(users_response):
    assert users_response.status_code == 200


def test_users_response_is_list(users_response):
    assert isinstance(users_response.json(), list)


def test_users_response_is_not_empty(users_response):
    assert len(users_response.json()) > 0


def test_users_response_each_user_has_id(users_response):
    for user in users_response.json():
        assert "id" in user


def test_users_response_each_user_has_email(users_response):
    for user in users_response.json():
        assert "email" in user


def test_users_response_all_ids_are_int(users_response):
    for user in users_response.json():
        assert isinstance(user["id"], int)


def test_environment_status_is_ready(test_environment):
    assert test_environment["status"] == "ready"


def test_environment_is_dict(test_environment):
    assert isinstance(test_environment, dict)


def test_environment_has_status_key(test_environment):
    assert "status" in test_environment


def test_environment_status_is_str(test_environment):
    assert isinstance(test_environment["status"], str)


def test_environment_setup_and_teardown_order(test_environment):
    print("Выполнение теста")
    assert test_environment == {"status": "ready"}
