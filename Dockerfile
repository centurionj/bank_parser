FROM python:3.12-slim

# USR_LOCAL_BIN - путь до пользовательских скриптов
# PROJECT_ROOT - путь до каталога внутри контейнера, в который будет
# копироваться приложение
ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/app

# Путь до исходников
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Пакеты для установки
ENV RUNTIME_PACKAGES="\
    libpcre3 \
    libjpeg-dev \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    bash \
    chromium \
    chromium-driver \
    libx11-6 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxi6 \
    fonts-dejavu \
    libnss3 \
    libfreetype6 \
    libharfbuzz0b \
    libgl1-mesa-glx"

# Пакеты для сборки
ENV BUILD_PACKAGES="\
    build-essential \
    libpcre3-dev \
    gcc"

# Установка базовых пакетов, обновление pip
RUN apt-get update && \
    apt-get upgrade -y && \
    pip install --upgrade pip

# Установка пакетов для сборки
RUN apt-get install -y --no-install-recommends $BUILD_PACKAGES

# Установка пакетов для runtime
RUN apt-get install -y --no-install-recommends $RUNTIME_PACKAGES

# Очистка кеша apt
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка переменных окружения для Chromium и Chromedriver
ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver \
    GOOGLE_CHROME_BIN=/usr/bin/chromium-browser

COPY src/requirements.txt $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT

# Установка зависимостей и удаление ненужных пакетов
RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove $BUILD_PACKAGES && \
    rm -rf /var/cache/apt/*

# Копируем скрипты и даем права на выполнение
COPY deploy/entrypoint.sh $USR_LOCAL_BIN/
COPY deploy/run_web.sh $USR_LOCAL_BIN/

RUN sed -i 's/\r//' $USR_LOCAL_BIN/*.sh \
    && chmod +x $USR_LOCAL_BIN/*.sh \
    && chmod +x $CHROMEDRIVER_BIN

# Копирование проекта
ADD src/ $PROJECT_ROOT/src/

# Копирование deploy в проект
ADD deploy/ $PROJECT_ROOT/deploy/

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
ENTRYPOINT ["run_web.sh"]
