import pytest
import requests

from config.settings import TIMEOUT


@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_existing_user_returns_200(base_url, user_id):
    response = requests.get(f"{base_url}/users/{user_id}", timeout=TIMEOUT)
    assert response.status_code == 200
    user = response.json()
    assert type(user["id"]) is int
    assert user["id"] == user_id
    assert "username" in user


@pytest.mark.parametrize("user_id", [999999, 888888, 777777])
def test_missing_user_returns_404(base_url, user_id):
    response = requests.get(f"{base_url}/users/{user_id}", timeout=TIMEOUT)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "resource, required_keys",
    [
        ("users", {"username"}),
        ("posts", {"userId", "body"}),
        ("comments", {"postId"}),
        ("todos", {"completed"}),
    ],
)
def test_resource_list_returns_200(base_url, resource, required_keys):
    response = requests.get(f"{base_url}/{resource}", timeout=TIMEOUT)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert items
    for item in items:
        assert isinstance(item, dict)
        assert required_keys <= item.keys()
        assert type(item["id"]) is int
        assert item["id"] > 0
