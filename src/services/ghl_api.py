import os
import json
from dotenv import load_dotenv
import requests as req

from src.logs.logging_config import logger
from src import DATADIR

load_dotenv()

BASEDIR = os.getcwd()


with open(os.path.join(BASEDIR, "src", "auth", ".ghl_tokens.json"), "r") as file:
    keys = json.load(file)


API_KEY = keys["api_key"]
LOCATION_ID = keys["locationId"]
ACCESS_TOKEN = keys["access_token"]
REFRESH_TOKEN = keys["refresh_token"]


class GHLApi:
    def __init__(self):
        self.url = "https://services.leadconnectorhq.com/"
        self.headers = {"Authorization": f"Bearer {ACCESS_TOKEN}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Version": "2021-07-28"}
        self.location_id = LOCATION_ID

    def create_conversation(self, contact_id):
        response = req.post(url=f"{self.url}conversations/",
                            headers=self.headers,
                            json={"locationId": self.location_id,
                                  "contactId": f"{contact_id}"})
        
        if response.status_code == 201:
            logger.info(f"SUCCESSFULLY CREATED GHL CONVERSATION FOR CONTACT: #{contact_id}")
            return response.json()["conversation"]["id"]
        else:
            logger.error(f"FAIL TO CREATE GHL CONVERSATION. ERROR: {response.text}")

    def add_inbound_message(self, conversation_id, message_text):
        data = {"type": "SMS",
                "conversationId": f"{conversation_id}",
                "message": f"{message_text}",
                "direction": "inbound"}

        response = req.post(url=f"{self.url}conversations/messages/inbound",
                            headers=self.headers,
                            json=data)
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"SUCCESSFULLY ADDED SMS NOTE TO CONVERSATION: #{conversation_id}")
            return response.json()
        else:
            logger.error(f"FAIL TO ADD INBOUND MESSAGE. ERROR: {response.text}")

    def set_sms_blast_status(self, contact_id: str, status: str = "Success"):
        data = {"customFields": [{"id": "KdiQPtxUnTXWEP4k0PW9",
                                  "value": status}]}

        response = req.put(url=f"{self.url}contacts/{contact_id}/",
                           headers=self.headers,
                           json=data)

        if response.status_code == 200:
            logger.info(f"SUCCESSFULLY SET SMS-BLAST STATUS FOR CONTACT: #{contact_id}")
            return response.json()
        else:
            logger.error(f"FAIL TO SET SMS-BLAST STATUS FOR CONTACT: #{contact_id}. "
                         f"ERROR: {response.text}")

    def get_contact_list(self):
        response = req.get(url=f"{self.url}contacts/",
                           headers=self.headers,
                           params={"locationId": self.location_id})
        
        if response.status_code == 200:
            logger.info(f"SUCCESSFULLY GOT CONTACTS LIST")
            return response.json()["contacts"]
        else:
            logger.error(f"FAIL TO GET CONTACTS LIST: {response.text}")


def ghl_processor(webhook_payload):
    GHL = GHLApi()
    CONTACTS_FILE = os.path.join(DATADIR, "test_data", "temp_test_contacts.json")

    from_number = webhook_payload["data"]["payload"]["from"]["phone_number"]
    message = webhook_payload["data"]["text"]

    with open(CONTACTS_FILE, "r") as f:
        contacts = json.load(f)
    for contact in contacts:
        contact_number = contact["Phone"]
        if contact_number == from_number:
            contact_id = contact_id["id"]
            conversation_id = GHL.create_conversation(contact_id=contact_id)
            if conversation_id:
                result = GHL.add_inbound_message(conversation_id=conversation_id,
                                                 message_text=message)
                return result
