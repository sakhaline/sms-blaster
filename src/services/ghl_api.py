import os
import json
from dotenv import load_dotenv
import requests as req

from src.logs.logging_config import logger


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


    def update_contact_tag(self, contact_id, tag):
        response = req.put(url=f"{self.url}contacts/{contact_id}",
                           headers=self.headers,
                           json={"tags": [tag]})

        if response.status_code == 200:
            logger.info(f"SUCCESSFULLY ADDED TAG {tag} TO THE CONTACT WITH ID: #{contact_id}")
            return True
        else:
            logger.error(f"FAIL TO UPDATE CONTACT TAG. ID: #{contact_id}. ERROR: {response.text}")


    def get_conversation_messages(self, conversation_id):
        response = req.get(url=f"{self.url}conversations/{conversation_id}/messages",
                           headers=self.headers)

        if response.status_code == 200:
            response_payload = response.json()
            logger.info(f"MESSAGES OF CONVERSAION WITH ID: {conversation_id} RECIEVED SUCCESSFULLY ^_^")
            return response_payload["messages"]["messages"]
        else:
            logger.error(f"FAIL TO GET CONVERSATION MESSAGES. ERROR: {response.text}.")


    def delete_conversation(self, conversation_id):
        response = req.delete(url=f"{self.url}conversations/{conversation_id}",
                                    headers=self.headers)

        if response.status_code == 200:
            logger.info(f"CONVERSAION WITH ID: {conversation_id} DELETED SUCCESSFULLY ^_^")
            return True
        else:
            logger.error(f"FAIL TO DELETE CONVERSATION MESSAGES. ERROR: {response.text}.")


    def update_contact_dnd(self, contact_id):
        data = {"dnd": True,
                "dndSettings": {"Call": {"status": "inactive"},
                                "Email": {"status": "inactive"},
                                "SMS": {"status": "inactive"},
                                "WhatsApp": {"status": "inactive"},
                                "GMB": {"status": "inactive"},
                                "FB":  {"status": "inactive"}}}
        response = req.put(url=f"{self.url}contacts/{contact_id}",
                           headers=self.headers,
                           json=data)

        if response.status_code == 200:
            logger.info(f"SUCCESSFULLY UPDATE CONTACT DND STATUS. CONTACT ID: #{contact_id}")
            return True
        else:
            logger.error(f"FAIL TO UPDATE DND STATUS. CONTACT ID: #{contact_id}. ERROR: {response.text}")

    def update_contact_tag(self, contact_id, tag):
        response = req.put(url=f"{self.url}contacts/{contact_id}",
                           headers=self.headers,
                           json={"tags": [tag]})

        if response.status_code == 200:
            logger.info(f"SUCCESSFULLY UPDATED CONTACT WITH TAG - {tag}. CONTACT ID: #{contact_id}")
            return True
        else:
            logger.error(f"FAIL TO UPDATE CONTACT WITH TAG - {tag}. CONTACT ID: #{contact_id}. ERROR: {response.text}")