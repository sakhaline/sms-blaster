from datetime import datetime
import time
from logging_config import logger
import phonenumbers
from pprint import pformat
import datetime
import csv
import json
import subprocess
from datetime import datetime


# datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
def execute_bash(commands):
    """
    executes bash commands
    """
    try:
        for command in commands:
            subprocess.run(command, shell=True, check=True)
            time.sleep(2)
    except subprocess.CalledProcessError as e:
        print(f"BASH ERROR - {e}")


csv_file_path = 'contacts.csv'
json_file_path = 'contacts.json'

"""
Contact Object:

    {
        "Contact Id": "Wpnqt7CXZAKnsqbSxgR6",
        "First Name": "Billy",
        "Last Name": "Smith",
        "Business Name": "Con Edison",
        "Company Name": "",
        "Phone": "+18005225635",
        "Email": "smithb@coned.com",
        "Created": "2024-01-14T19:48:47+02:00",
        "Last Activity": "",
        "Tags": "good email",
        "Additional Emails": "",
        "Additional Phones": "",
        "null": [
        ""
        ],

        "message": null,

        "telnyx_sent": false,
        "telnyx_delivered": false,
        "telnyx_message_id": null,

        "twilio_sent": false,
        "twilio_delivered": false,
        "twilio_message_id": null

        "ghl_sent": false,
        "ghl_delivered": false,

        "sms_delivered": false,

        "sms_sent_at": ""
    }
"""


def convert_csv_to_json(csv_path: str, json_path: str):
    """
    loads data from csv file and stores it into JSON
    output -> list[dict]
    file output -> .json
    """
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["message"] = None

            row["telnyx_sent"] = False
            row["telnyx_delivered"] = False
            row["telnyx_message_id"] = False

            row["twilio_sent"] = False
            row["twilio_delivered"] = False
            row["twilio_message_id"] = False

            row["ghl_sent"] = False
            row["ghl_delivered"] = False

            row["sms_delivered"] = False

            row["sms_sent_at"] = None

            data.append(row)

    with open(json_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)

    logging.info(
        f"{convert_csv_to_json.__name__} -- CONVERTED CSV [{csv_path}] TO JSON [{json_path}]")
    return data


def set_contact_sms_status(contacts_json_path: str, status: bool):
    """
    sets desired SMS sending status to each contact in .json with contacts
    """
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    for contact in contacts:
        logging.info(
            f"{set_contact_sms_status.__name__} -- CONTACT {contact.get('Contact Id')} STATUS CHANGED TO {status}")
        contact["sms_sent"] = status

    with open(contacts_json_path, "w") as f:
        json.dump(contacts, f)

    logging.info(
        f"{set_contact_sms_status.__name__} -- SAVED TO FILE - {contacts_json_path}")
    return True


def get_ids_by_phone(phone_numbers: list, contacts: list):
    """
    returns IDs of contacts, who have not received an SMS
    """
    ids = []

    for contact in contacts:
        if contact.get("Phone") in phone_numbers:
            ids.append(contact.get("Contact Id"))

    return ids


def convert_objects_to_string(json_file_path: str):
    with open(json_file_path, "r") as f:
        numbers = json.load(f)

    res = [f"+{number}" for number in numbers]

    with open(json_file_path, "w") as f:
        json.dump(res, f)


def prepare_statistics_report(result_json_path: str):
    with open(result_json_path, "r") as f:
        contacts = json.load(f)


    result = {
        "contacts_total": len(contacts),

        "contacts_sms_sent": 0,
        "contacts_sms_not_sent": 0,

        "telnyx_sent": 0,
        "twilio_sent": 0,
        "ghl_sent": 0,

        "telnyx_failed": 0,
        "twilio_failed": 0,
        "ghl_failed": 0,

        "date_time": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

    logging.info(f"{prepare_statistics_report.__name__} -- PREPARING SMS OUTREACH STATS FOR - {result['contacts_total']} - CONTACTS")


    for i, contact in enumerate(contacts, start=1):

        logging.info(f"{prepare_statistics_report.__name__} -- CONTACT # - {i}")

        if contact.get("sms_delivered") == True:
            result["contacts_sms_sent"] += 1

        if contact.get("sms_delivered") == False:
            result["contacts_sms_not_sent"] += 1

        if contact.get("telnyx_status") == True:
            result["telnyx_sent"] += 1

        if contact.get("twilio_status") == True:
            result["twilio_sent"] += 1

        if contact.get("ghl_status") == True:
            result["ghl_sent"] += 1

        if contact.get("telnyx_status") == False:
            result["telnyx_failed"] += 1

        if contact.get("twilio_status") == False:
            result["twilio_failed"] += 1

        if contact.get("ghl_status") == False:
            result["ghl_failed"] += 1

    with open("data/outreach_statistics.json", "r") as f:
        statistics_array: list = json.load(f)
        statistics_array.append(result)

    with open("data/outreach_statistics.json", "w") as f:
        json.dump(statistics_array, f)

    logging.info(f"{prepare_statistics_report.__name__} -- STATISTICS PREPARED - {pformat(result)}")

    return result


def format_phone_number(phone_number: str):
    """
    converts phone numbers to a desired format
    (012) 345-6789 -> +10123456789, etc.
    """
    phone_number_formatted = ""
    try:
        phone_number_formatted = phonenumbers.format_number(
            phonenumbers.parse(phone_number, 'US'),
            phonenumbers.PhoneNumberFormat.E164)
        logger.info(f"{format_phone_number.__name__} -- FORMATTED PHONE NUMBER -- FROM - {phone_number} - TO - {phone_number_formatted}")
    except Exception as ex:
        logger.warning(f"{format_phone_number.__name__} -- ! FAILED FORMATTING - {phone_number} - {ex}")
    return phone_number_formatted



if __name__ == "__main__":
    format_phone_number("1")
