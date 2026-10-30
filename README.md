# REST API Test Automation Framework

Автоматизированное тестирование REST API [JSONPlaceholder](https://jsonplaceholder.typicode.com) на Python: позитивные и негативные сценарии, проверка HTTP-статусов, JSON-структуры и query-параметров.

## Технологии

- Python 3.11+
- [pytest](https://docs.pytest.org/) — запуск и организация тестов
- [requests](https://requests.readthedocs.io/) — HTTP-клиент

## Структура проекта

```
├── tests/              # Тестовые сценарии (users, posts, comments, todos)
├── clients/            # API-клиент (HTTP-вызовы)
├── config/             # BASE_URL, TIMEOUT
├── conftest.py         # Общие фикстуры (base_url, api_client, …)
├── pytest.ini          # Настройки pytest
├── requirements.txt
└── README.md
```

## Установка

```bash
python -m pip install -r requirements.txt
```

Рекомендуется виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Запуск тестов

Из корня проекта:

```bash
python -m pytest -v
python -m pytest tests/test_users.py -v
```

## Покрытие сценариев

Реализовано **30 уникальных сценариев** по ТЗ:

| Блок | Файл | Сценарии |
|------|------|----------|
| Пользователи | `tests/test_users.py` | A-01 … A-08 |
| Публикации | `tests/test_posts.py` | B-01 … B-10 |
| Комментарии | `tests/test_comments.py` | C-01 … C-06 |
| Задачи | `tests/test_todos.py` | D-01 … D-06 |

Дополнительно: параметризованный тест `user_id ∈ {1, 2, 3}` и демонстрация фикстур `base_url`, `api_client`, `sample_post_payload`, `request_audit_log` (yield).

## Ограничение JSONPlaceholder

Сервис **не сохраняет** данные после POST, PUT, PATCH и DELETE. Тесты проверяют **ответ API** (статус и тело), но не постоянство изменений в «базе».

## Архитектурные решения

- **ApiClient** инкапсулирует URL, timeout и методы ресурсов — тесты не дублируют `requests.get(BASE_URL + ...)`.
- **config/settings.py** — единая точка для адреса и таймаута.
- **conftest.py** — фикстуры с `return` и `yield` для переиспользования между модулями.

## Возможные улучшения

1. Валидация контрактов через Pydantic 2 и Allure-отчёты.
2. CI (GitLab/GitHub Actions) и логирование запросов/ответов на уровне клиента.
