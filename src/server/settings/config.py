import os

from dotenv import load_dotenv

load_dotenv()

# Config for Account model
ACCOUNT_LIFETIME_MINUTES = 40
ACCOUNT_EXPIRATION_DELTA_DAY = 7

# URL for Go microservice
BASE_GO_API_URL = os.getenv('BASE_GO_API_URL', 'http://172.17.0.1:8080/api/v1/')

# Celery tasks delay
CELERY_TASK_DELAY_SEC = 2
