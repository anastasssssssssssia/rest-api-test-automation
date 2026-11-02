import requests

from config.settings import TIMEOUT


def test_get_post_returns_200(api_client):
    response = api_client.get_post(1)
    assert response.status_code == 200


def test_get_post_returns_requested_id(api_client):
    response = api_client.get_post(1)
    assert response.json()["id"] == 1


def test_get_post_has_required_fields(api_client):
    post = api_client.get_post(1).json()
    for field in ("userId", "id", "title", "body"):
        assert field in post


def test_get_post_field_types(api_client):
    post = api_client.get_post(1).json()
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)


def test_get_posts_returns_non_empty_list(api_client):
    posts = api_client.get_posts().json()
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_get_posts_filtered_by_user_id(api_client):
    posts = api_client.get_posts(params={"userId": 1}).json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


def test_create_post_returns_201_and_payload(api_client, sample_post_payload):
    response = api_client.create_post(sample_post_payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]


def test_update_post_returns_200_and_payload(api_client, sample_post_payload):
    response = api_client.update_post(1, sample_post_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]


def test_delete_post_returns_200(api_client):
    response = api_client.delete_post(1)
    assert response.status_code == 200


def test_get_nonexistent_post_returns_404(api_client):
    response = api_client.get_post(999999)
    assert response.status_code == 404


def test_base_url_get_post_1_returns_200(base_url):
    response = requests.get(f"{base_url}/posts/1", timeout=TIMEOUT)
    assert response.status_code == 200


def test_base_url_get_posts_returns_list(base_url):
    response = requests.get(f"{base_url}/posts", timeout=TIMEOUT)
    assert isinstance(response.json(), list)
