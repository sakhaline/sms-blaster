import csv
import json
from src.logs.logging_config import logger
import phonenumbers


def set_contact_sms_status(contacts_json_path: str, status: bool):
    """
    sets desired SMS sending status to each contact in .json with contacts
    """
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    for contact in contacts:
        logger.info(f"CONTACT {contact.get('Contact Id')} STATUS CHANGED TO {status}")
        contact["sms_sent"] = status

    with open(contacts_json_path, "w") as f:
        json.dump(contacts, f)

    logger.info(
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


def format_phone_number(phone_number: str):
    """
    converts phone numbers to a desired format
    (012) 345-6789 -> +10123456789 (add country code)
    +380671063839 -> +380671063839 (no change)
    """
    phone_number_formatted = ""
    try:
        phone_number_formatted = phonenumbers.format_number(
            phonenumbers.parse(phone_number, 'US'),
            phonenumbers.PhoneNumberFormat.E164)
        logger.info(f"FORMATTED PHONE NUMBER -- FROM - {phone_number} - TO - {phone_number_formatted}")
    except Exception as ex:
        logger.warning(f"FAILED FORMATTING - {phone_number} - {ex}")
    return phone_number_formatted


def insert_contact(db, scv_file_path):
    with open(scv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ghl_id = row["Contact Id"]
            fname = row["First Name"]
            lname = row["Last Name"]
            phone_number = row["Phone"]
            db.insert_contact(ghl_id, fname, lname, phone_number)
