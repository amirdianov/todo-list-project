# todo-list-project

## Техничсекое описание и требования

1. [Python версии не ниже 3.11](https://www.python.org/)

##  Инструкции по запуску

1. Вход в виртуальное окружение - `python3 -m venv venv`
2. Вход в виртуальное окружение - `source venv/bin/activate`
3. Установка зависимостей `pip install -r requirements.txt`
3. Поднять PostgreSQL с помощью Docker - `docker-compose up -d`
4. Выполнить миграции - `python manage.py migrate` 
5. Запуск сервера для разработки на http://localhost:8000 - `python manage.py runserver`


## Обозначения символов в коммитах

- `+` - добавлено
- `-` - удалено
- `=` - изменено
- `!` - исправлено
- `x%` - сделано на x процентов