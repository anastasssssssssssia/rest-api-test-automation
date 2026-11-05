import pytest
import requests

from config.settings import TIMEOUT


def test_get_user_returns_200(api_client):
    response = api_client.get_user(1)
    assert response.status_code == 200
    user = response.json()
    assert {"id", "name", "username", "email"} <= user.keys()
    assert type(user["id"]) is int
    assert user["id"] > 0


def test_get_user_returns_requested_id(api_client):
    user = api_client.get_user(1).json()
    assert type(user["id"]) is int
    assert user["id"] == 1
    assert "username" in user


def test_get_user_has_required_fields(api_client):
    user = api_client.get_user(1).json()
    for field in ("id", "name", "username", "email"):
        assert field in user


def test_get_user_field_types(api_client):
    user = api_client.get_user(1).json()
    assert type(user["id"]) is int
    assert user["id"] > 0
    assert isinstance(user["name"], str)
    assert isinstance(user["username"], str)
    assert isinstance(user["email"], str)


def test_get_user_address_contains_city(api_client):
    user = api_client.get_user(1).json()
    assert isinstance(user["address"], dict)
    assert "city" in user["address"]


def test_get_users_returns_non_empty_list(api_client):
    response = api_client.get_users()
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert users
    for user in users:
        assert {"id", "name", "username", "email"} <= user.keys()
        assert type(user["id"]) is int
        assert user["id"] > 0
        assert isinstance(user["email"], str)


def test_get_users_each_has_id_and_email(api_client):
    users = api_client.get_users().json()
    for user in users:
        assert type(user["id"]) is int
        assert user["id"] > 0
        assert isinstance(user["email"], str)
        assert "username" in user


def test_get_nonexistent_user_returns_404(api_client):
    response = api_client.get_user(999999)
    assert response.status_code == 404
    assert response.url.endswith("/users/999999")


def test_base_url_get_user_1_returns_200(base_url):
    response = requests.get(f"{base_url}/users/1", timeout=TIMEOUT)
    assert response.status_code == 200
    user = response.json()
    assert type(user["id"]) is int
    assert user["id"] == 1
    assert "username" in user


def test_base_url_get_user_2_returns_200(base_url):
    response = requests.get(f"{base_url}/users/2", timeout=TIMEOUT)
    assert response.status_code == 200
    user = response.json()
    assert type(user["id"]) is int
    assert user["id"] == 2
    assert "username" in user


def test_base_url_get_users_returns_list(base_url):
    response = requests.get(f"{base_url}/users", timeout=TIMEOUT)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert users
    for user in users:
        assert isinstance(user, dict)
        assert {"id", "name", "username", "email"} <= user.keys()
        assert type(user["id"]) is int
        assert user["id"] > 0


def test_user_response_status_code_is_200(user_response):
    assert user_response.status_code == 200
    assert "username" in user_response.json()


def test_user_response_body_is_valid_json(user_response):
    try:
        user = user_response.json()
    except requests.exceptions.JSONDecodeError:
        pytest.fail(f"Ответ не является JSON: {user_response.text!r}")
    assert "username" in user


def test_user_response_json_is_dict(user_response):
    user = user_response.json()
    assert isinstance(user, dict)
    assert "username" in user


def test_user_response_has_id(user_response):
    user = user_response.json()
    assert type(user["id"]) is int
    assert user["id"] > 0
    assert "username" in user


def test_user_response_has_name(user_response):
    user = user_response.json()
    assert isinstance(user["name"], str)
    assert "username" in user


def test_user_response_has_email(user_response):
    user = user_response.json()
    assert isinstance(user["email"], str)
    assert "username" in user


def test_user_json_id_is_two(user_json):
    assert type(user_json["id"]) is int
    assert user_json["id"] == 2
    assert "username" in user_json


def test_user_json_name_is_str(user_json):
    assert isinstance(user_json["name"], str)
    assert "username" in user_json


def test_user_json_name_is_not_empty(user_json):
    assert user_json["name"] != ""
    assert "username" in user_json


def test_user_json_has_email(user_json):
    assert "email" in user_json
    assert "username" in user_json


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
    users = users_response.json()
    assert isinstance(users, list)
    assert users
    assert all("username" in user for user in users)


def test_users_response_is_list(users_response):
    users = users_response.json()
    assert isinstance(users, list)
    assert users
    assert all("username" in user for user in users)


def test_users_response_is_not_empty(users_response):
    users = users_response.json()
    assert users
    assert all("username" in user for user in users)


def test_users_response_each_user_has_id(users_response):
    for user in users_response.json():
        assert type(user["id"]) is int
        assert user["id"] > 0
        assert "username" in user


def test_users_response_each_user_has_email(users_response):
    for user in users_response.json():
        assert isinstance(user["email"], str)
        assert "username" in user


def test_users_response_all_ids_are_int(users_response):
    for user in users_response.json():
        assert type(user["id"]) is int
        assert user["id"] > 0
        assert "username" in user
