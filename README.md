# REST API Test Automation

Автотесты REST API для [JSONPlaceholder](https://jsonplaceholder.typicode.com).
Python 3.11+, pytest, requests.

Репозиторий: [rest-api-test-automation](https://github.com/anastasssssssssssia/rest-api-test-automation)

## Установка

```bash
git clone https://github.com/anastasssssssssssia/rest-api-test-automation.git
cd rest-api-test-automation
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

В PowerShell активация: `.\.venv\Scripts\Activate.ps1`

## Запуск

Команды из корня проекта:

```bash
python -m pytest -v
python -m pytest -v -rs
python -m pytest tests/test_users.py -v
python -m pytest --collect-only -q
```

`-rs` показывает причины пропуска.

Ожидаемый результат прогона: все тесты зелёные, кроме помеченных маркерами.
`skip` и `skipif` дают SKIPPED, `xfail` даёт XFAIL или XPASS.

Тест с `RUN_SLOW` выполняется только при заданной переменной:

```bash
$env:RUN_SLOW = "1"
python -m pytest tests/test_skipif.py -v
```

Порядок setup → тест → teardown у фикстуры `test_environment`:

```bash
python -m pytest -s tests/test_users.py::test_environment_setup_and_teardown_order
```

## Структура

- `tests/` — тесты
- `conftest.py` — общие фикстуры
- `clients/api_client.py` — HTTP-клиент на `requests.Session`
- `config/settings.py` — `BASE_URL` и `TIMEOUT`
- `config/api_config.py` — `ApiConfig` и `StagingConfig`
- `helpers/user_helpers.py` — `UserValidator` и `double`
- `models/user.py` — модель `User`

## Фикстуры

| Фикстура | Scope | Что отдаёт |
| --- | --- | --- |
| `base_url` | session | адрес API |
| `api_client` | session | `ApiClient`, закрывается после прогона |
| `user_data` | function | словарь с данными пользователя |
| `user_response` | module | ответ `GET /users/1` |
| `user_json` | module | JSON `GET /users/2`, статус проверен |
| `users_response` | module | ответ `GET /users` |
| `test_environment` | function | `{"status": "ready"}` и печать до/после |
| `sample_post_payload` | function | тело для `POST` и `PUT /posts` |
| `temp_items` | function | временный список, очищается после теста |
| `cleanup_counter` | function | проверяет, что очистка `temp_items` прошла |
| `module_setup_state` | module | счётчик подготовок в модуле |

## Фикстура, декоратор и маркер

Фикстура — функция, которую pytest вызывает, чтобы подготовить данные
или ресурс для теста.

Декоратор — запись `@` над функцией. `@pytest.fixture` регистрирует функцию
как фикстуру. `@staticmethod`, `@classmethod` и `@property` к pytest
не относятся и задают поведение методов класса.

Маркер — метка `@pytest.mark.*` на тесте. `parametrize` задаёт наборы данных,
`skip` и `skipif` пропускают тест, `xfail` помечает ожидаемое падение.

Со `skip` тело теста не выполняется. Без маркера тест запускается
и проверяет `assert`. `xfail` тест запускает: падение даёт XFAIL,
успех — XPASS, а при `strict=True` успех становится FAIL.

## JSONPlaceholder

POST, PUT и DELETE не сохраняют данные на сервере.
В тестах проверяется только ответ API.

## Если что-то не так

- Тест упал с `ReadTimeout` или SSL-ошибкой — это сеть. Запусти тест ещё раз.
- Русские причины пропуска в PowerShell выглядят как «кракозябры» —
  выполни `chcp 65001` перед запуском.
