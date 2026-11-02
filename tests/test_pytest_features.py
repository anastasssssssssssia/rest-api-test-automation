import os
import sys

import pytest
import requests

from config.settings import TIMEOUT


@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_existing_user_returns_200(base_url, user_id):
    response = requests.get(f"{base_url}/users/{user_id}", timeout=TIMEOUT)
    assert response.status_code == 200


@pytest.mark.parametrize("user_id", [999999, 888888, 777777])
def test_missing_user_returns_404(base_url, user_id):
    response = requests.get(f"{base_url}/users/{user_id}", timeout=TIMEOUT)
    assert response.status_code == 404


@pytest.mark.parametrize("resource", ["users", "posts", "comments", "todos"])
def test_resource_list_returns_200(base_url, resource):
    response = requests.get(f"{base_url}/{resource}", timeout=TIMEOUT)
    assert response.status_code == 200


@pytest.mark.skip(reason="Функциональность не готова")
def test_user_avatar_is_uploaded(base_url):
    response = requests.post(
        f"{base_url}/users/1/avatar", json={"url": "avatar.png"}, timeout=TIMEOUT
    )
    assert response.status_code == 201


@pytest.mark.skip(reason="Временно отключён")
def test_patch_post_updates_title(base_url):
    response = requests.patch(f"{base_url}/posts/1", json={"title": "Patched"}, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["title"] == "Patched"


@pytest.mark.skipif(sys.platform == "win32", reason="Пропуск на Windows")
def test_posix_path_separator_is_slash():
    assert os.sep == "/"


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Требуется Python 3.11 или новее")
def test_tomllib_parses_config():
    import tomllib

    config = tomllib.loads('base_url = "https://example.com"')
    assert config == {"base_url": "https://example.com"}


@pytest.mark.xfail(reason="API не валидирует обязательные поля при создании поста")
def test_create_post_without_required_fields_returns_400(base_url):
    response = requests.post(f"{base_url}/posts", json={}, timeout=TIMEOUT)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Параметр _limit не описан в документации API", strict=False)
def test_posts_limit_parameter_restricts_result(base_url):
    response = requests.get(f"{base_url}/posts", params={"_limit": 5}, timeout=TIMEOUT)
    assert len(response.json()) == 5
