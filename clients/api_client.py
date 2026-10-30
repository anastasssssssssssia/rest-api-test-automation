import requests

from config.settings import BASE_URL, TIMEOUT


class ApiClient:
    """HTTP client for JSONPlaceholder REST API."""

    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_user(self, user_id: int) -> requests.Response:
        return requests.get(self._url(f"/users/{user_id}"), timeout=self.timeout)

    def get_users(self) -> requests.Response:
        return requests.get(self._url("/users"), timeout=self.timeout)

    def get_post(self, post_id: int) -> requests.Response:
        return requests.get(self._url(f"/posts/{post_id}"), timeout=self.timeout)

    def get_posts(self, params: dict | None = None) -> requests.Response:
        return requests.get(self._url("/posts"), params=params, timeout=self.timeout)

    def get_comments(self, params: dict | None = None) -> requests.Response:
        return requests.get(self._url("/comments"), params=params, timeout=self.timeout)

    def get_comment(self, comment_id: int) -> requests.Response:
        return requests.get(self._url(f"/comments/{comment_id}"), timeout=self.timeout)

    def get_todo(self, todo_id: int) -> requests.Response:
        return requests.get(self._url(f"/todos/{todo_id}"), timeout=self.timeout)

    def get_todos(self) -> requests.Response:
        return requests.get(self._url("/todos"), timeout=self.timeout)

    def create_post(self, payload: dict) -> requests.Response:
        return requests.post(self._url("/posts"), json=payload, timeout=self.timeout)

    def update_post(self, post_id: int, payload: dict) -> requests.Response:
        return requests.put(
            self._url(f"/posts/{post_id}"), json=payload, timeout=self.timeout
        )

    def delete_post(self, post_id: int) -> requests.Response:
        return requests.delete(self._url(f"/posts/{post_id}"), timeout=self.timeout)
