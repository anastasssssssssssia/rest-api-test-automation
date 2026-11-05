from clients.api_client import ApiClient
from config.api_config import ApiConfig, StagingConfig
from config.settings import BASE_URL


def test_from_environment_returns_api_config(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)
    config = ApiConfig.from_environment()
    assert type(config) is ApiConfig


def test_from_environment_reads_api_base_url(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://custom.example")
    config = ApiConfig.from_environment()
    assert config.base_url == "https://custom.example"


def test_api_client_uses_address_from_api_config(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://custom.example")
    client = ApiClient(base_url=ApiConfig.from_environment().base_url)
    sent = []

    def remember_url(url, **kwargs):
        sent.append(url)
        return None

    monkeypatch.setattr(client.session, "get", remember_url)
    monkeypatch.setattr(client.session, "post", remember_url)
    try:
        assert client.base_url == "https://custom.example"
        client.get_user(1)
        client.get_comment(1)
        client.get_todos()
        client.create_post({"title": "t", "body": "b", "userId": 1})
    finally:
        client.close()
    assert sent == [
        "https://custom.example/users/1",
        "https://custom.example/comments/1",
        "https://custom.example/todos",
        "https://custom.example/posts",
    ]


def test_from_environment_uses_default_base_url(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)
    config = ApiConfig.from_environment()
    assert config.base_url == BASE_URL


def test_subclass_from_environment_returns_subclass_instance(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)
    config = StagingConfig.from_environment()
    assert type(config) is StagingConfig
    assert config.base_url == StagingConfig.default_base_url


def test_subclass_attribute_change_is_used_and_restored(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)
    original = StagingConfig.default_base_url
    with monkeypatch.context() as patch:
        patch.setattr(StagingConfig, "default_base_url", "https://changed.example")
        config = StagingConfig.from_environment()
        assert type(config) is StagingConfig
        assert config.base_url == "https://changed.example"
        assert ApiConfig.default_base_url == BASE_URL
    assert StagingConfig.from_environment().base_url == original
