import os
import json
from src import DATADIR
from src.services.telnyx_service import TelnyxService
from src.services.ghl_service import GHLService
from src.logs.logging_config import logger
from src.data.messages import MESSAGE1


TELNYX = TelnyxService()
GHL = GHLService()
contacts_file = os.path.join(DATADIR, "test_data", "temp_test_contacts.json")


def telnyx_sender(contact, from_number, message):
    to_number = contact["Phone"]
    if to_number:
        sms_id = TELNYX.send_sms(to_number=to_number,
                                 from_number=from_number,
                                 sms_message=message)
        if sms_id:
            contact["telnyx_sent"] = True
            contact["telnyx_message_id"] = sms_id
            logger.info("TELNYX CONTACT UPDATED SUCCESSFULLY!!! ^_^")


def telnyx_sms_status_checker(contacts_file):
    flag = True
    with open(contacts_file, "r") as f:
        all_contacts = json.load(f)

        for contact in all_contacts:
            if contact["telnyx_message_id"]:
                sms_id = contact["telnyx_message_id"]
                status = TELNYX.check_delivery_status(sms_id)
                if status == "dlivered":
                    contact["telnyx_delivered"] = True
                elif status in ["queued", "sending", "sent"]:
                    flag = False
    with open(contacts_file, "w") as f:
        json.dump(all_contacts, f, indent=4)
    return flag


def ghl_sender(contact):
    contact_id = contact["id"]
    inbound_message = contact["inbound_message"]
    conversation_id = GHL.create_conversation(contact_id=contact_id)
    if conversation_id:
        status = GHL.add_inbound_message(conversation_id=conversation_id, message=inbound_message)
        if status:
            contact["ghl_sent"] = True
            contact["ghl_delivered"] = True
            logger.info("GHL CONTACT UPDATED SUCCESSFULLY!!! ^_^")


def telnyx_processor():
    from_number = "+19172031898"
    message = MESSAGE1
    with open(contacts_file, "r") as f:
        contacts = json.load(f)
    for contact in contacts:
        telnyx_sender(contact, from_number, message)

    with open(contacts_file, "w") as f:
        json.dump(contacts, f, indent=4)

    flag = telnyx_sms_status_checker(contacts_file)
    while not flag:
        flag = telnyx_sms_status_checker(contacts_file)


if __name__ == "__main__":
    telnyx_processor()
