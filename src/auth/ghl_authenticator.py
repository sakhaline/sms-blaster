import os
import json
import requests
import datetime
from src.logs.logging_config import logger


cwd = os.getcwd()

def refresh_auth_token(tokens_json_path: str):
    """
    refreshes GHL authentication token
    updates .json with tokens
    """
    with open(tokens_json_path, "r") as file:
        get_keys = json.load(file)

    response = requests.post(
        url="https://services.leadconnectorhq.com/oauth/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        data={
            "client_id": get_keys["client_id"],
            "client_secret": get_keys["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": get_keys["refresh_token"]
        }
    )
    if response.status_code == 200:

        with open(tokens_json_path, "w") as file:
            get_keys["access_token"] = response.json()["access_token"]
            get_keys["refresh_token"] = response.json()["refresh_token"]
            get_keys["refreshed_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
            json.dump(get_keys, file, indent=4)
        logger.info("Token refreshed successfully!!! ^_^")
    else:
        logger.error("Failed to refresh token")


if __name__ == "__main__":
    refresh_auth_token("/home/sakhaline/ACTSE/davydov/sms_blaster/src/auth/.ghl_tokens.json")