FROM python:3.12-alpine

# USR_LOCAL_BIN - путь до пользовательских скриптов
# PROJECT_ROOT - путь до каталога внутри контейнера, в который будет
# копироваться приложение
ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/app

# путь до исходников
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Пакеты, которые необходимы для работы в runtime
ENV RUNTIME_PACKAGES="\
    libev \
    pcre \
    jpeg-dev \
    zlib-dev \
    libressl-dev \
    libffi-dev \
    bash \
    chromium \
    chromium-chromedriver \
    libx11 \
    libxcomposite \
    libxrandr \
    libxdamage \
    libxi \
    ttf-freefont \
    nss \
    freetype \
    harfbuzz \
    mesa-gl \
    xvfb-run"


# Пакеты, которые необходимы для установки зависимостей.
# Не останутся в итоговом образе.
ENV BUILD_PACKAGES="\
    libev-dev \
    build-base \
    pcre-dev \
    gcc \
    linux-headers"

# Установка пакетов, обновление pip
RUN apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    apk --no-cache add --virtual build-deps $BUILD_PACKAGES && \
    apk --no-cache add $RUNTIME_PACKAGES

# Установка переменных окружения для Chromium и Chromedriver
ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver \
    GOOGLE_CHROME_BIN=/usr/bin/chromium-browser

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
    && chmod +x $USR_LOCAL_BIN/*.sh \
    && chmod +x $CHROMEDRIVER_BIN

# копирование непосредственно проекта
ADD src/ $PROJECT_ROOT/src/

# Копирование src/server/static/ только если такая директория существует
RUN if [ -d "$PROJECT_ROOT/src/server/static" ]; then \
        cp -r $PROJECT_ROOT/src/server/static/ $PROJECT_ROOT/src/server/static/; \
    fi

# Копирование deploy в проект
ADD deploy/ $PROJECT_ROOT/deploy/

# Настройка прав доступа для взаимодействия с X11 удалить после тестов
RUN apk add --no-cache mesa-gl mesa-dri-gallium && \
    mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Установка переменной окружения для передачи X11 удалить после тестов
ENV DISPLAY=:99

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

ENTRYPOINT ["run_web.sh"]