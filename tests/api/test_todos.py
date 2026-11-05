import requests

from config.settings import TIMEOUT


def test_get_todo_returns_200(api_client):
    response = api_client.get_todo(1)
    assert response.status_code == 200
    todo = response.json()
    assert {"userId", "id", "title", "completed"} <= todo.keys()
    assert type(todo["id"]) is int
    assert todo["id"] > 0
    assert type(todo["userId"]) is int
    assert isinstance(todo["title"], str)
    assert isinstance(todo["completed"], bool)


def test_get_todo_returns_requested_id(api_client):
    todo = api_client.get_todo(1).json()
    assert type(todo["id"]) is int
    assert todo["id"] == 1
    assert isinstance(todo["completed"], bool)


def test_get_todo_has_required_fields(api_client):
    todo = api_client.get_todo(1).json()
    for field in ("userId", "id", "title", "completed"):
        assert field in todo


def test_get_todo_completed_is_bool(api_client):
    todo = api_client.get_todo(1).json()
    assert isinstance(todo["completed"], bool)


def test_get_todos_returns_valid_tasks(api_client):
    response = api_client.get_todos()

    assert response.status_code == 200

    todos = response.json()
    assert isinstance(todos, list)
    assert todos, "API вернул пустой список задач"

    for todo in todos:
        assert isinstance(todo, dict)
        assert {"id", "userId", "title", "completed"} <= todo.keys()

        assert type(todo["id"]) is int
        assert todo["id"] > 0
        assert type(todo["userId"]) is int
        assert isinstance(todo["title"], str)
        assert isinstance(todo["completed"], bool)


def test_get_nonexistent_todo_returns_404(api_client):
    response = api_client.get_todo(999999)
    assert response.status_code == 404
    assert response.url.endswith("/todos/999999")


def test_base_url_get_todo_1_returns_200(base_url):
    response = requests.get(f"{base_url}/todos/1", timeout=TIMEOUT)
    assert response.status_code == 200
    todo = response.json()
    assert type(todo["id"]) is int
    assert todo["id"] == 1
    assert isinstance(todo["completed"], bool)


def test_base_url_get_todos_returns_list(base_url):
    response = requests.get(f"{base_url}/todos", timeout=TIMEOUT)
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert todos
    for todo in todos:
        assert isinstance(todo, dict)
        assert {"id", "userId", "title", "completed"} <= todo.keys()
        assert type(todo["id"]) is int
        assert todo["id"] > 0
        assert type(todo["userId"]) is int
        assert isinstance(todo["title"], str)
        assert isinstance(todo["completed"], bool)
