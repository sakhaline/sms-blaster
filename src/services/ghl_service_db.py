from src.db.api import DBAPI
from src.logs.logging_config import logger
from src.services.ghl_api import GHLApi


class GHLService:
    def __init__(self):
        self.ghl_api = GHLApi()
        self.db = DBAPI()

    def define_tag(self, message: str):
        tag = ""
        if message.lower().strip() == "stop":
            tag = "no contact"
        else:
            tag = "active"
        return tag


    def ghl_processor(self, webhook_payload):
        from_number = webhook_payload["data"]["payload"]["from"]["phone_number"]
        if from_number not in ["+16297580157", "+16297580011", "+19016761096"]:
            logger.debug(webhook_payload["data"])
            message = webhook_payload["data"]["payload"]["text"]

            contact_id = self.db.get_ghl_id_by_phone_number(from_number)
            conversation_id = self.ghl_api.create_conversation(contact_id=contact_id)
            if conversation_id:
                result = self.ghl_api.add_inbound_message(conversation_id=conversation_id,
                                                          message_text=message)
                if result:
                    tag = self.define_tag
                    if tag == "no contact":
                        self.db.update_ghl_conversation_info(contact_id=contact_id,
                                                             conversation_id=conversation_id,
                                                             message=message,
                                                             conversation_status=0)
                        self.ghl_api.delete_conversation(conversation_id)
                    else:
                        self.db.update_ghl_conversation_info(contact_id=contact_id,
                                                            conversation_id=conversation_id,
                                                            message=message)