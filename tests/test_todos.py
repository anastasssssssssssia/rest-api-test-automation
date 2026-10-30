def test_d01_get_todo_one_returns_200(api_client):
    """D-01: GET /todos/1 -> HTTP 200."""
    response = api_client.get_todo(1)
    assert response.status_code == 200


def test_d02_get_todo_one_id_equals_one(api_client):
    """D-02: GET /todos/1 -> id = 1."""
    response = api_client.get_todo(1)
    assert response.json()["id"] == 1


def test_d03_get_todo_one_has_required_fields(api_client):
    """D-03: GET /todos/1 -> userId, id, title, completed present."""
    todo = api_client.get_todo(1).json()
    for field in ("userId", "id", "title", "completed"):
        assert field in todo


def test_d04_get_todo_one_completed_is_bool(api_client):
    """D-04: GET /todos/1 -> completed is bool."""
    todo = api_client.get_todo(1).json()
    assert isinstance(todo["completed"], bool)


def test_d05_get_todos_returns_non_empty_list(api_client):
    """D-05: GET /todos -> non-empty list."""
    todos = api_client.get_todos().json()
    assert isinstance(todos, list)
    assert len(todos) > 0


def test_d06_get_nonexistent_todo_returns_404(api_client):
    """D-06: GET /todos/999999 -> HTTP 404."""
    response = api_client.get_todo(999999)
    assert response.status_code == 404
