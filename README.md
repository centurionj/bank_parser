# Серверная часть парсера

## Стэк

- Python 3.12
- Django 5.1.4
- PostgreSQL
- Docker
- Docker-compose
- Swagger
- nginx
- Gunicorn
- bash
- Celery
- Celery-beat
- Redis

## Описание проекта

Парсер транзакций из лк банка.

## Инструкция по развертыванию

Создать .env из .env.example

#### Параметры приложения

| Ключ                     | Значение                        | Примечания                                                      |
|--------------------------|---------------------------------|-----------------------------------------------------------------|
| `DJANGO_SETTINGS_MODULE` | Модуль настроек Django          | В проде указывааем server.settings.prod                         |
| `DEBUG`                  | Режим запуска                   | В проде указывааем False                                        |
| `TIME_ZONE`              | Временная зона сервера          | *                                                               |
| `ALLOWED_HOSTS`          | Разрешенные хосты               | Можно оставить *                                                |
| `POSTGRES_DB`            | Имя базы данных pg              | Должен быть отличный от postgres                                |
| `POSTGRES_USER`          | Имя пользователя базы данных pg | Должен быть отличный от postgres                                |
| `POSTGRES_PASSWORD`      | Пароль к базе данных pg         | Должен быть отличный от postgres                                |
| `POSTGRES_HOST`          | Хост базы данных pg             | Если запуск через докер то ставим postgres, ручками - localhost |
| `POSTGRES_PORT`          | Порт базы данных pg             | По умолчанию 5432                                               |
| `REDIS_HOST`             | Хост базы данных redis          | *                                                               |
| `REDIS_PORT`             | Порт базы данных redis          | По умолчанию 6379                                               |
| `BACK_DOMAIN`            | Домен серверной части           | *                                                               |
| `FRONT_DOMAIN`           | Домен фронта                    | *                                                               |
| `TG_LINK`                | Ссылка на разраба               | Указывается в футере админке                                    |

### Запуск через докер

1. В корне проекта

```shell
docker-compose up --build
```

2. Суперюзер создастся автоматически. Учетные данные login/password: admin/admin

### Запуск вручную

1. В PgAdmin4 создать базу данных
2. Выполнить миграции

```shell
python manage.py migrate
```

3. Запустить проект

```shell
python manage.py runserver
```

4. Создать супер-пользователя джанго

```shell
python manage.py createsuperuser
```

### Запуск для разработки

1. В корне проекта

```shell
docker-compose up db redis
```

2. Выполнить миграции

```shell
python manage.py migrate
```

3. Создать супер-пользователя джанго

```shell
python manage.py createsuperuser
```

4. Запустить проект

```shell
python manage.py runserver
```

### Документация к api (SWAGGER)

http://localhost:8000/api/v1/swagger/ или http://localhost/api/v1/swagger/

### Линтеры и качество кода

```shell
cd src/server/
flake8
isort .
```
