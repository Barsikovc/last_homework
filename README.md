# Homework — Django REST Framework

Учебный проект по курсу DRF. Реализован API для работы с пользователями.

## Требования

- Python 3.10+
- pip

## Установка и запуск

1. Клонировать репозиторий:
   ```bash
   git clone <ссылка-на-репозиторий>
   cd homework
   ```

2. Создать и активировать виртуальное окружение:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Применить миграции:
   ```bash
   python manage.py migrate
   ```

5. (Опционально) Создать суперпользователя для админки:
   ```bash
   python manage.py createsuperuser
   ```

6. Запустить сервер:
   ```bash
   python manage.py runserver
   ```

## Доступные адреса

- API пользователей: http://127.0.0.1:8000/api/users/
- Регистрация: http://127.0.0.1:8000/api/users/register/
- Swagger: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/
- Админка: http://127.0.0.1:8000/admin/