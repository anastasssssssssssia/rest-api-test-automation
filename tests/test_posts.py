def test_b01_get_post_one_returns_200(api_client):
    """B-01: GET /posts/1 -> HTTP 200."""
    response = api_client.get_post(1)
    assert response.status_code == 200


def test_b02_get_post_one_id_equals_one(api_client):
    """B-02: GET /posts/1 -> id = 1."""
    response = api_client.get_post(1)
    assert response.json()["id"] == 1


def test_b03_get_post_one_has_required_fields(api_client):
    """B-03: GET /posts/1 -> userId, id, title, body present."""
    post = api_client.get_post(1).json()
    for field in ("userId", "id", "title", "body"):
        assert field in post


def test_b04_get_post_one_field_types(api_client):
    """B-04: GET /posts/1 -> correct types for required fields."""
    post = api_client.get_post(1).json()
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)


def test_b05_get_posts_returns_non_empty_list(api_client):
    """B-05: GET /posts -> non-empty list."""
    posts = api_client.get_posts().json()
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_b06_get_posts_filtered_by_user_id(api_client):
    """B-06: GET /posts?userId=1 -> all items have userId = 1."""
    posts = api_client.get_posts(params={"userId": 1}).json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


def test_b07_create_post_returns_201_and_payload(api_client, sample_post_payload):
    """B-07: POST /posts -> HTTP 201, id present, fields match payload."""
    response = api_client.create_post(sample_post_payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]


def test_b08_update_post_returns_200_and_payload(api_client, sample_post_payload):
    """B-08: PUT /posts/1 -> HTTP 200, fields match payload."""
    response = api_client.update_post(1, sample_post_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == sample_post_payload["title"]
    assert body["body"] == sample_post_payload["body"]
    assert body["userId"] == sample_post_payload["userId"]


def test_b09_delete_post_returns_200(api_client):
    """B-09: DELETE /posts/1 -> HTTP 200 (persistence not checked)."""
    response = api_client.delete_post(1)
    assert response.status_code == 200


def test_b10_get_nonexistent_post_returns_404(api_client):
    """B-10: GET /posts/999999 -> HTTP 404."""
    response = api_client.get_post(999999)
    assert response.status_code == 404
