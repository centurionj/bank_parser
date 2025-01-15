import os

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_LIFETIME_MINUTES = 40
ACCOUNT_EXPIRATION_DELTA_DAY = 7

BASE_GO_API_URL = os.getenv('BASE_GO_API_URL', 'http://localhost:8080/api/v1/')
