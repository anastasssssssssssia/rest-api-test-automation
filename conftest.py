import pytest

from clients.api_client import ApiClient
from config.api_config import ApiConfig

pytest_plugins = ("pytester",)

setup_calls_by_module: dict[str, int] = {}


@pytest.fixture(scope="session")
def base_url() -> str:
    return ApiConfig.from_environment().base_url


@pytest.fixture(scope="session")
def api_client(base_url: str):
    client = ApiClient(base_url=base_url)
    yield client
    client.close()


@pytest.fixture(scope="function")
def user_data() -> dict:
    return {
        "id": 1,
        "name": "Anna",
        "email": "anna@example.com",
        "age": 25,
        "active": True,
    }


@pytest.fixture(scope="module")
def user_response(api_client: ApiClient):
    return api_client.get_user(1)


@pytest.fixture(scope="module")
def user_json(api_client: ApiClient) -> dict:
    response = api_client.get_user(2)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="module")
def users_response(api_client: ApiClient):
    return api_client.get_users()


@pytest.fixture
def test_environment():
    print("Подготовка окружения")
    yield {"status": "ready"}
    print("Завершение работы")


@pytest.fixture
def sample_post_payload() -> dict:
    return {"title": "Test title", "body": "Test body", "userId": 1}


@pytest.fixture
def cleanup_counter():
    counter = {"cleanups": 0}
    yield counter
    assert counter["cleanups"] == 1, "Очистка temp_items не выполнилась"


@pytest.fixture
def temp_items(cleanup_counter: dict):
    items = ["temp"]
    yield items
    items.clear()
    cleanup_counter["cleanups"] += 1


@pytest.fixture(scope="module")
def module_setup_state(request):
    module_name = request.module.__name__
    setup_calls_by_module[module_name] = setup_calls_by_module.get(module_name, 0) + 1
    return {"setups": setup_calls_by_module[module_name]}
