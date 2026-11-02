import requests

from config.settings import TIMEOUT


def test_get_comments_returns_200(api_client):
    response = api_client.get_comments()
    assert response.status_code == 200


def test_get_comments_returns_non_empty_list(api_client):
    comments = api_client.get_comments().json()
    assert isinstance(comments, list)
    assert len(comments) > 0


def test_get_comments_have_required_fields(api_client):
    comments = api_client.get_comments().json()
    for comment in comments:
        for field in ("postId", "id", "name", "email", "body"):
            assert field in comment


def test_get_comments_field_types(api_client):
    comments = api_client.get_comments().json()
    for comment in comments:
        assert isinstance(comment["postId"], int)
        assert isinstance(comment["id"], int)
        assert isinstance(comment["name"], str)
        assert isinstance(comment["email"], str)
        assert isinstance(comment["body"], str)


def test_get_comments_filtered_by_post_id(api_client):
    comments = api_client.get_comments(params={"postId": 1}).json()
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)


def test_get_nonexistent_comment_returns_404(api_client):
    response = api_client.get_comment(999999)
    assert response.status_code == 404


def test_base_url_get_comment_1_returns_200(base_url):
    response = requests.get(f"{base_url}/comments/1", timeout=TIMEOUT)
    assert response.status_code == 200
