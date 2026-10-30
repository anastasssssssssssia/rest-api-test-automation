import pytest

from config.settings import BASE_URL


def test_a01_get_user_one_returns_200(api_client):
    """A-01: GET /users/1 -> HTTP 200."""
    response = api_client.get_user(1)
    assert response.status_code == 200


def test_a02_get_user_one_id_equals_one(api_client):
    """A-02: GET /users/1 -> id = 1."""
    response = api_client.get_user(1)
    assert response.json()["id"] == 1


def test_a03_get_user_one_has_required_fields(api_client):
    """A-03: GET /users/1 -> id, name, username, email present."""
    user = api_client.get_user(1).json()
    for field in ("id", "name", "username", "email"):
        assert field in user


def test_a04_get_user_one_field_types(api_client):
    """A-04: GET /users/1 -> correct field types."""
    user = api_client.get_user(1).json()
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["username"], str)
    assert isinstance(user["email"], str)


def test_a05_get_user_one_address_contains_city(api_client):
    """A-05: GET /users/1 -> address is dict with city."""
    user = api_client.get_user(1).json()
    assert isinstance(user["address"], dict)
    assert "city" in user["address"]


def test_a06_get_users_returns_non_empty_list(api_client):
    """A-06: GET /users -> non-empty list."""
    users = api_client.get_users().json()
    assert isinstance(users, list)
    assert len(users) > 0


def test_a07_get_users_each_has_id_and_email(api_client):
    """A-07: GET /users -> each user has id and email."""
    users = api_client.get_users().json()
    for user in users:
        assert "id" in user
        assert "email" in user


def test_a08_get_nonexistent_user_returns_404(api_client):
    """A-08: GET /users/999999 -> HTTP 404."""
    response = api_client.get_user(999999)
    assert response.status_code == 404


def test_base_url_matches_settings(base_url):
    """Fixture demo: base_url is shared configuration."""
    assert base_url == BASE_URL


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_by_id_parametrized(api_client, user_id, request_audit_log):
    """Parametrized: GET /users/{id} -> HTTP 200 and matching id."""
    request_audit_log.append(f"user-{user_id}")
    response = api_client.get_user(user_id)
    assert response.status_code == 200
    assert response.json()["id"] == user_id
