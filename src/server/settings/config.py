import os

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_LIFETIME_MINUTES = 40
ACCOUNT_EXPIRATION_DELTA_DAY = 7

ALPHA_LOGIN_URL = os.getenv('ALPHA_LOGING_URL', '')
