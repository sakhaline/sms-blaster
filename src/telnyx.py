import os
import json
import requests
from logging_config import logger
from datetime import datetime
import utils.utils as utils


    # [{"message": "",
    # "telnyx_sent": false,
    # "telnyx_delivered": false,
    # "telnyx_message_id": "null",
    # "twilio_sent": false,
    # "twilio_delivered": false,
    # "twilio_message_id": false,
    # "ghl_sent": false,
    # "ghl_delivered": false,
    # "sms_delivered": false,
    # "sms_sent_at": "null"}]


API_KEY = os.getenv("TELNYX_API_KEY")
PUBLIC_KEY = os.getenv("TELNYX_PUBLIC_KEY")


def send_telnyx_sms(phone_number, sms_message: str, from_number):
    """
    sends single SMS message with Telnyx
    """
    phone_number_validated = utils.format_phone_number(phone_number)

    logger.info(f"{send_telnyx_sms.__name__} -- TELNYX - SENDING SMS TO - {phone_number} FROM - {from_number}")

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
    logger.info(f"{send_telnyx_sms.__name__} -- TELNYX - STATUS CODE -- {status_code}")

    result = {
        "success": True if status_code == 200 else False, 
        "data": None,
        "message_id": None
        }

    try:
        response_data = response.json()
        logger.info(f"{send_telnyx_sms.__name__} -- TELNYX - RESPONSE DATA -- {response_data}")

        result["data"] = response_data["data"]
        result["message_id"] = response_data["data"]["id"]
    except Exception as ex:
        logger.error(f"{send_telnyx_sms.__name__} -- !!! TELNYX ERROR -- {ex}")

    return result["success"]


def update_contacts(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
    for contact in data:
        contact["telnyx_sent"] = False
        contact["telnyx_sent_at"] = 0
    return data


def format_message(contact_name):
    sms_message = ("Hi)!\nThis is Bill, "
                "Director of Business Lending at CAPLOA. We can get you "
                "approved within one hour for Capital for your business "
                "and get the money in your bank today!\n\nInterested Just Respond YES\n")
    if contact_name:
        sms_message = sms_message.replace(")", f" {contact_name}")
    else:
        sms_message = sms_message.replace(")", "")
    return sms_message


def check_telnyx_delivery_status(message_id):
    logger.info(f"{check_telnyx_delivery_status.__name__} -- CHECKING TELNYX DELIVERY STATUS FOR - {message_id}")

    response = requests.get(
        url=f"https://api.telnyx.com/v2/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
            }
        )
    status_code = response.status_code
    delivery_status = None
    logger.info(f"{check_telnyx_delivery_status.__name__} -- TELNYX STATUS CODE -- {status_code}")

    try:
        response_data = response.json()
        logger.info(f"{check_telnyx_delivery_status.__name__} -- TELNYX RESPONSE DATA -- {response_data}")

        delivery_status = response_data["data"]["to"][-1]["status"]
    except Exception as ex:
        logger.error(f"{check_telnyx_delivery_status.__name__} -- !!! TELNYX ERROR -- {ex}")

    return True if delivery_status == "delivered" else False


def main(input_file, output_file):
    raw_data = update_contacts(input_file)

    with open(output_file, "w") as f:
        json.dump(raw_data, f, indent=4)

    for contact in raw_data:
        contact_id = contact.get("Contact Id", "")
        contact_name = contact.get("First Name", "")
        msg = format_message(contact_name)

        sent_status = send_telnyx_sms(contact_id, msg)
        if sent_status:
            contact["telnyx_sent"] = True
            contact["telnyx_sent_at"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            with open(output_file, "w") as f:
                json.dump(raw_data, f, indent=4)
                logger.info(f"{main.__name__} -- DATA DUMPED SUCCESSFULLY")


if __name__ == "__main__":
    message = "Test"
    input_file = "/home/sakhaline/ACTSE/frylow/sms_blaster/src/data/temp_test_contacts.json"
    output_file = "/home/sakhaline/ACTSE/frylow/sms_blaster/src/data/processed_contacts.json"
    main(input_file, output_file)
