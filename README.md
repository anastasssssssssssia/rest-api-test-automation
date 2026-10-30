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

## Запуск тестов

```bash
python -m pytest -v
python -m pytest tests/test_users.py -v
```

## JSONPlaceholder

POST, PUT и DELETE не сохраняют данные на сервере.
В тестах проверяется только ответ API.
