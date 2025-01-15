import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.html import format_html
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_ROOT = BASE_DIR.parent

SECRET_KEY = get_random_secret_key()

INSTALLED_APPS = [
    # админ
    'jazzmin',

    # стандартные
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # установленные библиотеки
    'drf_yasg',
    'django_celery_beat',
    'rest_framework',

    # приложения
    'server.apps.accounts',
    'server.apps.payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv('BACK_DOMAIN', ''),
    os.getenv('FRONT_DOMAIN', ''),
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        # 'HOST': 'localhost',
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'ru-RU')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'server/static')
STATICFILES_DIR = [STATIC_DIR]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(SOURCES_ROOT, 'server/static')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# REDIS_HOST = 'localhost'
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# celery

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

# celery beat

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Celery tasks

CELERY_DISCOVER_TASKS = [
    'server.tasks.account_tasks',
    'server.tasks.bank_auth_tasks',
]

# DRF
REST_FRAMEWORK = {
    'DEFAULT_RENDER_CLASSES': (
        'rest_framework.renders.JSONRenderer',
        'rest_framework.renders.BrowsableAPIRenderer',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Swagger
SWAGGER_SETTINGS = {
    'api_version': 'v1',
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
    },
}

# Jazzmin
JAZZMIN_SETTINGS = {
    'site_title': 'Парсер транзакций',
    'site_header': 'Парсер транзакций',
    'site_brand': 'Парсер транзакций',
    "welcome_sign": "WEB-приложение для парсинга банковских транзакций",
    "copyright": format_html(f'<a href="{os.getenv("TG_LINK", "")}">Разработка и поддержка Карпухин Михаил</a>'),
}

# Домен
FRONT_DOMAIN = os.getenv('FRONT_DOMAIN', 'http://localhost:3000')
BACK_DOMAIN = os.getenv('BACK_DOMAIN', 'http://localhost:8000')

SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
