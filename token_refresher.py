import os
import time
import schedule
from src.logs.logging_config import logger
from src.auth.ghl_authenticator import refresh_auth_token


cwd = os.getcwd()


def refresher():
    secret_path = os.path.join(cwd, "src", "auth", ".ghl_tokens.json")
    refresh_auth_token(secret_path)


schedule.every(6).hours.do(refresher)

while True:
    schedule.run_pending()
    time.sleep(1)
