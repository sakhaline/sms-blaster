import os
import random
from dotenv import load_dotenv
import requests as req
import json

from src.logs.logging_config import logger
from src.services.telnyx_api import TelnyxApi
import src.utils.utils as utils
from data.messages import MESSAGE1
from . import CONTACTS_FILE

load_dotenv()


class TelnyxService:
    def __init__(self):
        self.telnyx_api = TelnyxApi()
        self.numbers = ["+16297580157", "+16297580011", "+19016761096"]

    def get_contacts(self):
        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)
            return contacts

    def dump_contacts(self, contacts):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(contacts, f, indent=4)

    def telnyx_sender(self, from_number, contact, message):
        to_number = contact["phone"]
        if to_number:
            sms_id = self.telnyx_api.send_sms(to_number=to_number,
                                              from_number=from_number,
                                              sms_message=message)
            if sms_id:
                contact["telnyx_sent"] = True
                contact["telnyx_message_id"] = sms_id
                logger.info("TELNYX CONTACT UPDATED SUCCESSFULLY!!! ^_^")

    def telnyx_sms_status_checker(self):
        flag = True
        contacts = self.get_contacts()

        for contact in contacts:
            if contact["telnyx_message_id"]:
                sms_id = contact["telnyx_message_id"]
                status = self.telnyx_api.check_delivery_status(sms_id)
                if status == "delivered":
                    contact["telnyx_delivered"] = True
                elif status in ["queued", "sending", "sent"]:
                    flag = False

        self.dump_contacts(contacts)
        return flag

    def telnyx_processor(self):
        from_number = random.choice(self.numbers)
        print(from_number)

        message = MESSAGE1
        contacts = self.get_contacts()

        for contact in contacts:
            self.telnyx_sender(contact=contact, from_number=from_number, message=message)

        self.dump_contacts(contacts)

        flag = self.telnyx_sms_status_checker()
        while not flag:
            flag = self.telnyx_sms_status_checker()
