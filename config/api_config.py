import os

from config.settings import BASE_URL


class ApiConfig:
    default_base_url = BASE_URL

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @classmethod
    def from_environment(cls) -> "ApiConfig":
        base_url = os.environ.get("API_BASE_URL", cls.default_base_url)
        return cls(base_url)


class StagingConfig(ApiConfig):
    default_base_url = "https://staging.example.com"
