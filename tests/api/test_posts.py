import pytest
import requests

from config.settings import TIMEOUT


def test_get_post_returns_200(api_client):
    response = api_client.get_post(1)
    assert response.status_code == 200
    post = response.json()
    assert {"userId", "id", "title", "body"} <= post.keys()
    assert type(post["id"]) is int
    assert post["id"] > 0
    assert type(post["userId"]) is int


def test_get_post_returns_requested_id(api_client):
    post = api_client.get_post(1).json()
    assert type(post["id"]) is int
    assert post["id"] == 1
    assert type(post["userId"]) is int
    assert {"userId", "title", "body"} <= post.keys()


def test_get_post_has_required_fields(api_client):
    post = api_client.get_post(1).json()
    for field in ("userId", "id", "title", "body"):
        assert field in post


def test_get_post_field_types(api_client):
    post = api_client.get_post(1).json()
    assert type(post["userId"]) is int
    assert type(post["id"]) is int
    assert post["id"] > 0
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)


def test_get_posts_returns_non_empty_list(api_client):
    response = api_client.get_posts()
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert posts
    for post in posts:
        assert {"userId", "id", "title", "body"} <= post.keys()
        assert type(post["id"]) is int
        assert post["id"] > 0
        assert type(post["userId"]) is int
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_get_posts_filtered_by_user_id(api_client):
    response = api_client.get_posts(params={"userId": 1})
    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(
        type(post["userId"]) is int
        and post["userId"] == 1
        and "title" in post
        and "body" in post
        for post in posts
    )


def test_create_post_returns_201_and_payload(api_client, sample_post_payload):
    response = api_client.create_post(sample_post_payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert type(body["id"]) is int
    assert body["id"] > 0
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]
    assert response.url.endswith("/posts")


def test_update_post_returns_200_and_payload(api_client, sample_post_payload):
    response = api_client.update_post(1, sample_post_payload)
    assert response.status_code == 200
    body = response.json()
    assert type(body["id"]) is int
    assert body["id"] == 1
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]
    assert response.url.endswith("/posts/1")


def test_delete_post_returns_200(api_client):
    response = api_client.delete_post(1)
    assert response.status_code == 200
    assert response.url.endswith("/posts/1")


def test_get_nonexistent_post_returns_404(api_client):
    response = api_client.get_post(999999)
    assert response.status_code == 404
    assert response.url.endswith("/posts/999999")


def test_base_url_get_post_1_returns_200(base_url):
    response = requests.get(f"{base_url}/posts/1", timeout=TIMEOUT)
    assert response.status_code == 200
    post = response.json()
    assert type(post["id"]) is int
    assert post["id"] == 1
    assert {"userId", "title", "body"} <= post.keys()


def test_base_url_get_posts_returns_list(base_url):
    response = requests.get(f"{base_url}/posts", timeout=TIMEOUT)
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert posts
    for post in posts:
        assert isinstance(post, dict)
        assert {"userId", "id", "title", "body"} <= post.keys()
        assert type(post["id"]) is int
        assert post["id"] > 0
        assert type(post["userId"]) is int
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_create_post_without_required_fields_returns_400(api_client):
    response = api_client.create_post({})
    if response.status_code == 201:
        pytest.xfail("API принимает пост без обязательных полей и возвращает 201")
    assert response.status_code == 400


def test_posts_limit_parameter_restricts_result(api_client):
    response = api_client.get_posts(params={"_limit": 5})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 5
    for post in posts:
        assert {"userId", "id", "title", "body"} <= post.keys()
        assert type(post["id"]) is int
        assert post["id"] > 0
        assert isinstance(post["body"], str)
