import json
import requests
from logging_config import logger
from datetime import datetime

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

with open("auth/.ghl_tokens.json", "r") as file:
    keys = json.load(file)


API_KEY = keys["api_key"]
LOCATION_ID = keys["location_id"]
ACCESS_TOKEN = keys["access_token"]
REFRESH_TOKEN = keys["refresh_token"]


def send_sms_ghl(contact_id: str, message: str):
    """
    sends single SMS message with GHL
    """
    BASE_URL = f"https://services.leadconnectorhq.com/conversations/messages"
    HEADERS = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Version': '2021-04-15'
    }
    PAYLOAD = {
        "type": "SMS",
        "contactId": contact_id,
        "message": message
    }
    response = requests.post(url=BASE_URL, headers=HEADERS, json=PAYLOAD)
    
    
    status_code = response.status_code
    logger.info(f"{send_sms_ghl.__name__} -- GHL - STATUS CODE -- {status_code}")
    result = False

    try:
        response_data = response.json()
        logger.info(f"{send_sms_ghl.__name__} -- GHL RESPONSE - {response_data}")

        result = True if status_code in (201, 200) else False
    except Exception as ex:
        logger.error(f"{send_sms_ghl.__name__} -- !!! GHL ERROR - {ex}")

    return result


def update_contacts(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    for contact in data:
        contact["ghl_sent"] = False
        contact["ghl_sent_at"] = 0

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


def main(input_file, output_file):
    raw_data = update_contacts(input_file)

    with open(output_file, "w") as f:
        json.dump(raw_data, f, indent=4)

    for contact in raw_data:
        contact_id = contact.get("Contact Id", "")
        contact_name = contact.get("First Name", "")
        msg = format_message(contact_name)

        sent_status = send_sms_ghl(contact_id, msg)
        if sent_status:
            contact["ghl_sent"] = True
            contact["ghl_sent_at"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            with open(output_file, "w") as f:
                json.dump(raw_data, f, indent=4)
                logger.info(f"{main.__name__} -- DATA DUMPED SUCCESSFULLY")


if __name__ == "__main__":
    message = "Test"
    input_file = "/home/sakhaline/ACTSE/frylow/sms_blaster/src/data/temp_test_contacts.json"
    output_file = "/home/sakhaline/ACTSE/frylow/sms_blaster/src/data/processed_contacts.json"
    main(input_file, output_file)
    # send_sms_ghl("FBC7Lmslsd29qVJOjWTW", message)