from random import randint
import os
from dotenv import load_dotenv
import requests
from pprint import pprint
from logging_config import logger as logging
import utils.utils as utils


API_KEY = os.getenv("TELNYX_API_KEY")
PUBLIC_KEY = os.getenv("TELNYX_PUBLIC_KEY")


def check_telnyx_delivery_status(message_id):
    logging.info(f"{check_telnyx_delivery_status.__name__} -- CHECKING TELNYX DELIVERY STATUS FOR - {message_id}")

    response = requests.get(
        url=f"https://api.telnyx.com/v2/messages/{message_id}", 
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
            }
        )

    status_code = response.status_code
    delivery_status = None
    logging.info(f"{check_telnyx_delivery_status.__name__} -- TELNYX STATUS CODE -- {status_code}")

    try:
        response_data = response.json()
        logging.info(f"{check_telnyx_delivery_status.__name__} -- TELNYX RESPONSE DATA -- {response_data}")

        delivery_status = response_data["data"]["to"][-1]["status"]
    except Exception as ex:
        logging.error(f"{check_telnyx_delivery_status.__name__} -- !!! TELNYX ERROR -- {ex}")

    return True if delivery_status == "delivered" else False


def send_telnyx_sms(phone_number, sms_message: str, from_number):
    """
    sends single SMS message with Telnyx
    """
    phone_number_validated = utils.format_phone_number(phone_number)

    logging.info(f"{send_telnyx_sms.__name__} -- TELNYX - SENDING SMS TO - {phone_number} FROM - {from_number}")

    response = requests.post(
        url="https://api.telnyx.com/v2/messages",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "type": "SMS",
            "text": f"{sms_message}",
            "from": from_number,
            "to": phone_number_validated
        }
    )


    status_code = response.status_code
    logging.info(f"{send_telnyx_sms.__name__} -- TELNYX - STATUS CODE -- {status_code}")

    result = {
        "success": True if status_code == 200 else False, 
        "data": None,
        "message_id": None
        }

    try:
        response_data = response.json()
        logging.info(f"{send_telnyx_sms.__name__} -- TELNYX - RESPONSE DATA -- {response_data}")

        result["data"] = response_data["data"]
        result["message_id"] = response_data["data"]["id"]
    except Exception as ex:
        logging.error(f"{send_telnyx_sms.__name__} -- !!! TELNYX ERROR -- {ex}")

    return result


if __name__ == "__main__":
    pass
