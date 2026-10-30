import pytest

from clients.api_client import ApiClient
from config.settings import BASE_URL


@pytest.fixture
def base_url() -> str:
    """Shared base URL for tests that need the configured endpoint."""
    return BASE_URL


@pytest.fixture
def api_client(base_url: str) -> ApiClient:
    """API client bound to the configured base URL."""
    return ApiClient(base_url=base_url)


@pytest.fixture
def sample_post_payload() -> dict:
    """Reusable POST /posts body for create/update scenarios."""
    return {"title": "Test title", "body": "Test body", "userId": 1}


@pytest.fixture
def request_audit_log():
    """Collects scenario markers during a test; cleared after the test finishes."""
    log: list[str] = []
    yield log
    log.clear()
