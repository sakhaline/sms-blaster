import os
import json
from dotenv import load_dotenv
import requests as req

from src.logs.logging_config import logger
from src.services.ghl_api import GHLApi
from . import CONTACTS_FILE


class GHLService:
    def __init__(self):
        self.ghl_api = GHLApi()

    def get_contacts(self):
        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)
        return contacts

    def dump_contacts(self, contacts):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(contacts, f, indent=4)

    def ghl_processor(self, webhook_payload):
        from_number = webhook_payload["data"]["payload"]["from"]["phone_number"]
        logger.debug(webhook_payload["data"])
        mwssage_id = webhook_payload["data"]["payload"]["id"]
        message = webhook_payload["data"]["payload"]["text"]
        contacts = self.get_contacts()

        for contact in contacts:
            contact_number = contact["Phone"]
            if contact_number == from_number:
                logger.debug(f"CONTACT HAS SENT MESSAGE: {contact}")
                contact_id = contact["Contact Id"]
                conversation_id = self.ghl_api.create_conversation(contact_id=contact_id)
                if conversation_id:
                    result = self.ghl_api.add_inbound_message(conversation_id=conversation_id,
                                                              message_text=message)
                    if result:
                        contact["telnyx_message_id"] = mwssage_id
                        contact["message"] = message
                        contact["ghl_sent"] = True
                        contact["ghl_delivered"] = True
                        logger.info("GHL CONTACT UPDATED SUCCESSFULLY!!! ^_^")
                self.dump_contacts(contacts)
                break
