from logging_config import logger
from auth.ghl_authenticator import refresh_auth_token
from utils.bash_utils import execute_bash
from datetime import datetime
import time
import services.services as sms
from statistics import prepare_statistics_report


def main(contacts_json_path: str):
    """
    the main function;
    entry point for the complete system
    """

    # if refresh_auth_token("auth/ghl_tokens.json"):
    #     logging.info(f"{main.__name__} -- REFRESHED GHL AUTH TOKEN")
    logger.info(f"{main.__name__} -- STARTING BULK SMS OUTREACH")

    # major functionality execution
    sms.sms_blaster(contacts_json_path)


if __name__ == "__main__":
    main("data/test_contacts.json")

    # execute_bash(['echo Test',
    #      'git add .',
    #      f'git commit -m "autocommit {datetime.utcnow().strftime("%Y_%m_%d__%H_%M")}"',
    #      'git push origin main'
    #      ])
