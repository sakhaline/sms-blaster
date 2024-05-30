import os
from celery_config import app
from src.auth import AUTHDATA_DIR
from src.auth.ghl_authenticator import refresh_auth_token


cwd = os.getcwd()


@app.task
def refresh_auth_token_task():
    secret_path = os.path.join(cwd, "src", "auth", ".ghl_tokens.json")
    refresh_auth_token(secret_path)
    return "Token refreshed successfully!!! ^_^"


"""
celery -A tasks beat --loglevel=info
celery -A tasks worker --loglevel=info
"""