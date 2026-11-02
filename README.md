# REST API Test Automation

Автотесты REST API [JSONPlaceholder](https://jsonplaceholder.typicode.com).
Python 3.11+, pytest, requests.

## Установка

```powershell
git clone https://github.com/anastasssssssssssia/rest-api-test-automation.git
cd rest-api-test-automation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Запуск

Команды из корня проекта:

```powershell
python -m pytest -v
python -m pytest tests/test_users.py -v
```

В полном прогоне есть skipped, xfailed и xpassed.
failed быть не должно.

## Структура

- `tests/` тесты
- `conftest.py` общие фикстуры
- `clients/api_client.py` HTTP-клиент
- `config/settings.py` адрес API и таймаут
- `config/api_config.py` конфигурация API
- `helpers/user_helpers.py` проверки данных пользователя
- `models/user.py` модель пользователя

## JSONPlaceholder

POST, PUT и DELETE не сохраняют данные на сервере.
Тесты проверяют только ответ API.
