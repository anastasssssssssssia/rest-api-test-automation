import os
import sys

import pytest
import requests

from config.settings import TIMEOUT


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


@pytest.mark.xfail(reason="пример неожиданного успеха", strict=False)
def test_xpass_when_marked_check_passes():
    assert 2 * 2 == 4
