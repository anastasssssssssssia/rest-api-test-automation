import requests

from config.settings import TIMEOUT


def test_get_comments_returns_200(api_client):
    response = api_client.get_comments()
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert comments
    for comment in comments:
        assert isinstance(comment, dict)
        assert type(comment["id"]) is int
        assert comment["id"] > 0
        assert type(comment["postId"]) is int
        assert "body" in comment


def test_get_comments_returns_non_empty_list(api_client):
    response = api_client.get_comments()
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert comments, "API вернул пустой список комментариев"
    for comment in comments:
        assert isinstance(comment, dict)
        assert {"postId", "id", "name", "email", "body"} <= comment.keys()
        assert type(comment["postId"]) is int
        assert type(comment["id"]) is int
        assert comment["id"] > 0
        assert isinstance(comment["name"], str)
        assert isinstance(comment["email"], str)
        assert isinstance(comment["body"], str)


def test_get_comments_have_required_fields(api_client):
    comments = api_client.get_comments().json()
    for comment in comments:
        for field in ("postId", "id", "name", "email", "body"):
            assert field in comment


def test_get_comments_field_types(api_client):
    comments = api_client.get_comments().json()
    for comment in comments:
        assert type(comment["postId"]) is int
        assert type(comment["id"]) is int
        assert comment["id"] > 0
        assert isinstance(comment["name"], str)
        assert isinstance(comment["email"], str)
        assert isinstance(comment["body"], str)


def test_get_comments_filtered_by_post_id(api_client):
    response = api_client.get_comments(params={"postId": 1})
    assert response.status_code == 200
    comments = response.json()
    assert comments
    assert all(
        type(comment["postId"]) is int and comment["postId"] == 1 and "body" in comment
        for comment in comments
    )


def test_get_comment_returns_requested_comment(api_client):
    response = api_client.get_comment(1)

    assert response.status_code == 200

    comment = response.json()
    assert isinstance(comment, dict)
    assert type(comment["id"]) is int
    assert comment["id"] == 1
    assert type(comment["postId"]) is int
    assert {"postId", "name", "email", "body"} <= comment.keys()


def test_get_nonexistent_comment_returns_404(api_client):
    response = api_client.get_comment(999999)
    assert response.status_code == 404
    assert response.url.endswith("/comments/999999")


def test_base_url_get_comment_1_returns_200(base_url):
    response = requests.get(f"{base_url}/comments/1", timeout=TIMEOUT)
    assert response.status_code == 200
    comment = response.json()
    assert type(comment["id"]) is int
    assert comment["id"] == 1
    assert {"postId", "name", "email", "body"} <= comment.keys()
