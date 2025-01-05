FROM python:3.12-alpine

# USR_LOCAL_BIN - путь до пользовательских скриптов
# PROJECT_ROOT - путь до каталога внутри контейнера, в который будет
# копироваться приложение
ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/app

# путь до исходников
# ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# пакеты, которые необходимы для работы в runtime
ENV RUNTIME_PACKAGES="\
    libev \
    pcre \
    jpeg-dev \
    zlib-dev \
    libressl-dev \
    libffi-dev"


# Пакеты, которые необходимы для установки зависимостей.
# Не останутся в итоговом образе.
ENV BUILD_PACKAGES="\
    libev-dev \
    build-base \
    pcre-dev \
    gcc \
    build-base \
    linux-headers"

# Установка пакетов, обновление pip, создание директорий
RUN apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    apk --no-cache add --virtual build-deps $BUILD_PACKAGES && \
    apk --no-cache add $RUNTIME_PACKAGES


COPY src/requirements.txt $PROJECT_ROOT/


WORKDIR $PROJECT_ROOT

# Установка зависимостей и удаление ненужных пакетов
RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps && \
    rm -rf /var/cache/apk/* && \
    rm -rf /var/lib/apt/lists/*


# Копируем скрипты и даем права на выполнение
COPY deploy/entrypoint.sh $USR_LOCAL_BIN/
COPY deploy/run_web.sh $USR_LOCAL_BIN/

RUN sed -i 's/\r//' $USR_LOCAL_BIN/*.sh \
    && chmod +x $USR_LOCAL_BIN/*.sh

# копирование непосредственно проекта
ADD src/ $PROJECT_ROOT/src/

# Копирование src/server/static/ только если такая директория существует
RUN if [ -d "$PROJECT_ROOT/src/server/static" ]; then \
        cp -r $PROJECT_ROOT/src/server/static/ $PROJECT_ROOT/src/server/static/; \
    fi

# Копирование deploy в проект
ADD deploy/ $PROJECT_ROOT/deploy/

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

ENTRYPOINT ["run_web.sh"]