import pytest


@pytest.fixture
def environment_events():
    events = []
    yield events
    assert events == ["setup", "test", "teardown"]


@pytest.fixture
def tracked_environment(environment_events):
    print("Подготовка окружения")
    environment_events.append("setup")
    yield {"status": "ready"}
    print("Завершение работы")
    environment_events.append("teardown")


def test_environment_status_is_ready(test_environment):
    assert test_environment["status"] == "ready"


def test_environment_is_dict(test_environment):
    assert isinstance(test_environment, dict)


def test_environment_has_status_key(test_environment):
    assert "status" in test_environment


def test_environment_status_is_str(test_environment):
    assert isinstance(test_environment["status"], str)


def test_environment_setup_and_teardown_order(tracked_environment, environment_events):
    print("Выполнение теста")
    environment_events.append("test")
    assert environment_events == ["setup", "test"]
    assert tracked_environment == {"status": "ready"}
