import os
import json
from dotenv import load_dotenv
import requests as req
from src.db.api import DBAPI

from src.logs.logging_config import logger
from src.services.ghl_api import GHLApi



class GHLService:
    def __init__(self, db):
        self.ghl_api = GHLApi()
        self.db = DBAPI()

    def ghl_processor(self, webhook_payload):
        from_number = webhook_payload["data"]["payload"]["from"]["phone_number"]
        logger.debug(webhook_payload["data"])
        message = webhook_payload["data"]["payload"]["text"]

        contact_id = self.db.get_ghl_id_by_phone_number(from_number)
        conversation_id = self.ghl_api.create_conversation(contact_id=contact_id)
        if conversation_id:
            result = self.ghl_api.add_inbound_message(conversation_id=conversation_id,
                                                      message_text=message)
            if result:
                self.db.update_ghl_conversation_info(contact_id=contact_id,
                                                     conversation_id=conversation_id,
                                                     message=message)
