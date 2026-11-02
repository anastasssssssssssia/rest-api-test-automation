import pytest
import requests

from config.settings import TIMEOUT
from helpers.user_helpers import double


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_by_id_returns_matching_user(api_client, user_id):
    response = api_client.get_user(user_id)
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.parametrize("value, expected", [(2, 4), (3, 6), (5, 10)])
def test_double_returns_twice_the_value(value, expected):
    assert double(value) == expected


@pytest.mark.parametrize(
    "field, expected_type",
    [("id", int), ("name", str), ("address", dict)],
)
def test_user_field_has_expected_type(api_client, field, expected_type):
    user = api_client.get_user(1).json()
    assert isinstance(user[field], expected_type)


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_posts_are_filtered_by_user_id(api_client, user_id):
    posts = api_client.get_posts(params={"userId": user_id}).json()
    assert len(posts) > 0
    assert all(post["userId"] == user_id for post in posts)


@pytest.mark.parametrize("resource", ["users", "posts", "todos"])
def test_missing_resource_returns_404(base_url, resource):
    response = requests.get(f"{base_url}/{resource}/999999", timeout=TIMEOUT)
    assert response.status_code == 404
