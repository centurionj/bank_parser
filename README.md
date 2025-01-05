# Серверная часть AR приложения для компании “Бот Сад”

## Стэк

- Python 3.10
- Django 5.0.3
- PostgreSQL
- Docker
- Docker-compose
- Swagger
- nginx
- Gunicorn
- bash

## Описание проекта

Программное обеспечение с элементами виртуальной реальности (VR), позволяющее клиентам
визуализировать вывеску на своем объекте.
Пользователь получает макет вывески и может с помощью мобильного устройства
навести камеру на объект, чтобы перенести макет вывески на него,
выбрав подходящий масштаб и место.

![img.png](doc/img.png)

## Инструкция по развертыванию

Создать .env из .env.example

#### Параметры приложения

| Ключ                | Значение                     | Примечания                                                      |
|---------------------|------------------------------|-----------------------------------------------------------------|
| `DEBUG`             | Режим запуска                | В проде указывааем False                                        |
| `TIME_ZONE`         | Временная зона сервера       | *                                                               |
| `ALLOWED_HOSTS`     | Разрешенные хосты            | Можно оставить *                                                |
| `POSTGRES_DB`       | Имя базы данных              | Должен быть отличный от postgres                                |
| `POSTGRES_USER`     | Имя пользователя базы данных | Должен быть отличный от postgres                                |
| `POSTGRES_PASSWORD` | Пароль к базе данных         | Должен быть отличный от postgres                                |
| `POSTGRES_HOST`     | Хост базы данных             | Если запуск через докер то ставим postgres, ручками - localhost |
| `POSTGRES_PORT`     | Порт базы данных             | По умолчанию 5432                                               |
| `BACK_DOMAIN`       | Домен серверной части        | *                                                               |
| `FRONT_DOMAIN`      | Домен фронта                 | *                                                               |
| `KINZA_SITE`        | Сайт kinza                   | Указывается в футере админке                                    |

### Запуск через докер

1. В корне проекта

```shell
docker-compose up --build
```

Затем создать супер-пользователя Django. В новом терминале выполнить команды по очереди:

```shell
docker ps

docker exec -it <id_контейнера_web> bash

cd src/

python manage.py createsuperuser
```

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
docker-compose up postgres
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
