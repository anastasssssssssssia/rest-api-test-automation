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
