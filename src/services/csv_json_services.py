import csv
import json
from logging_config import logger
import utils.utils as utils
import services.ghl_services as ghl


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

    logger.info(
        f"{convert_csv_to_json.__name__} -- CONVERTED CSV [{csv_path}] TO JSON [{json_path}]")
    return data


def set_contact_sms_status(contacts_json_path: str, status: bool):
    """
    sets desired SMS sending status to each contact in .json with contacts
    """
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    for contact in contacts:
        logger.info(
            f"{set_contact_sms_status.__name__} -- CONTACT {contact.get('Contact Id')} STATUS CHANGED TO {status}")
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


if __name__ == "__main__":
    convert_csv_to_json("data/contacts.csv", "data/contacts.json")
    # convert_objects_to_string("data/failed_numbers.json")

    # with open("data/contacts.json", "r") as f:
    #     all_contacts = json.load(f)

    # with open("data/failed_numbers.json", "r") as f:
    #     failed_numbers = json.load(f)

    # with open("data/successful_numbers.json", "r") as f:
    #     successful_numbers = json.load(f)

    # failed_ids = get_ids_by_phone(failed_numbers, all_contacts)
    # successful_ids = get_ids_by_phone(successful_numbers, all_contacts)

    # print("Failed: ", failed_ids)
    # print()
    # print("Successful: ", successful_ids)



    # # print("\n\n== Setting failed status")
    # # print()
    # # for i, contact_id in enumerate(failed_ids):

    # #     if i < 5: input('>> ')

    # #     try:

    # #         ghl.set_ghl_sms_blast_status(contact_id, "Failed")

    # #         get_conversations_response = ghl.get_conversations(contact_id)

    # #         conversation = get_conversations_response["result"]["conversations"][0]
    # #         conversation_id = conversation["id"]

    # #         ghl.delete_conversation(conversation_id)

    # #     except Exception as ex:
    # #         logging.error(f"!!! ERROR -- {ex}")

    # print("\n\n== Setting success status")
    # print()
    # for contact_id in successful_ids:
    #     ghl.set_ghl_sms_blast_status(contact_id, "Success")