def test_c01_get_comments_returns_200(api_client):
    """C-01: GET /comments -> HTTP 200."""
    response = api_client.get_comments()
    assert response.status_code == 200


def test_c02_get_comments_returns_non_empty_list(api_client):
    """C-02: GET /comments -> non-empty list."""
    comments = api_client.get_comments().json()
    assert isinstance(comments, list)
    assert len(comments) > 0


def test_c03_get_comments_have_required_fields(api_client):
    """C-03: GET /comments -> postId, id, name, email, body present."""
    comments = api_client.get_comments().json()
    for comment in comments[:5]:
        for field in ("postId", "id", "name", "email", "body"):
            assert field in comment


def test_c04_get_comments_field_types(api_client):
    """C-04: GET /comments -> correct types for required fields."""
    comment = api_client.get_comments().json()[0]
    assert isinstance(comment["postId"], int)
    assert isinstance(comment["id"], int)
    assert isinstance(comment["name"], str)
    assert isinstance(comment["email"], str)
    assert isinstance(comment["body"], str)


def test_c05_get_comments_filtered_by_post_id(api_client):
    """C-05: GET /comments?postId=1 -> all items have postId = 1."""
    comments = api_client.get_comments(params={"postId": 1}).json()
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)


def test_c06_get_nonexistent_comment_returns_404(api_client):
    """C-06: GET /comments/999999 -> HTTP 404."""
    response = api_client.get_comment(999999)
    assert response.status_code == 404
