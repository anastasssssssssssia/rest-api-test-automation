import pytest

from clients.api_client import ApiClient


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_by_id_returns_matching_user(api_client, user_id):
    response = api_client.get_user(user_id)
    assert response.status_code == 200
    user = response.json()
    assert type(user["id"]) is int
    assert user["id"] == user_id
    assert "username" in user


@pytest.mark.parametrize(
    "field, expected_type",
    [("id", int), ("name", str), ("address", dict)],
)
def test_user_field_has_expected_type(api_client, field, expected_type):
    user = api_client.get_user(1).json()
    assert "username" in user
    if expected_type is int:
        assert type(user[field]) is int
    else:
        assert isinstance(user[field], expected_type)


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_posts_are_filtered_by_user_id(api_client, user_id):
    response = api_client.get_posts(params={"userId": user_id})
    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(
        type(post["userId"]) is int
        and post["userId"] == user_id
        and "title" in post
        and "body" in post
        for post in posts
    )


@pytest.mark.parametrize(
    "method_name, path",
    [
        ("get_user", "/users/999999"),
        ("get_post", "/posts/999999"),
        ("get_todo", "/todos/999999"),
        ("get_comment", "/comments/999999"),
    ],
)
def test_missing_resource_returns_404(api_client: ApiClient, method_name, path):
    response = getattr(api_client, method_name)(999999)
    assert response.status_code == 404
    assert response.url.endswith(path)
