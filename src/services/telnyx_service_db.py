import os
from time import sleep
import random
from dotenv import load_dotenv


from src.logs.logging_config import logger
from src.services.telnyx_api import TelnyxApi
from data.messages import MESSAGE1
from src.db.api import DBAPI

load_dotenv()


class TelnyxService:
    def __init__(self, start, end):
        self.telnyx_api = TelnyxApi()
        self.numbers = ["+16297580157", "+16297580011", "+19016761096"]
        self.db = DBAPI()
        self.start = start
        self.end = end


    def telnyx_sender(self, from_number, contact_number, message):
        if contact_number:
            sms_id = self.telnyx_api.send_sms(to_number=contact_number,
                                              from_number=from_number,
                                              sms_message=message)
            if sms_id:
                return sms_id
        else:
            logger.warning(f"CONTACT HAS NO NUMBER")


    def telnyx_processor(self):
        from_number = random.choice(self.numbers)
        sms_id = None
        message = MESSAGE1
        contacts = self.db.get_phone_number_telnyx_status_list(self.start, self.end)
        for contact in contacts:
            try:
                status = contact[1]
                contact_number = contact[0]
            except IndexError:
                logger.error(f"FAIL TO SEND SMS. NO NECESSARY FIELDS.")
            else:
                if status == 0:
                    sms_id = self.telnyx_sender(contact_number=contact_number,
                                                from_number=from_number,
                                                message=message)
                if sms_id:
                    self.db.update_telnyx_sent_sms_id_by_phone_number(phone_number=contact_number,
                                                                      sms_id=sms_id)
                sleep(1)
        # flag = self.telnyx_sms_status_checker()
        # while not flag:
        #     flag = self.telnyx_sms_status_checker()

    # def telnyx_sms_status_checker(self):
    #     flag = True
    #     contacts = self.get_contacts()

    #     for contact in contacts:
    #         if contact["telnyx_message_id"]:
    #             sms_id = contact["telnyx_message_id"]
    #             status = self.telnyx_api.check_delivery_status(sms_id)
    #             if status == "delivered":
    #                 contact["telnyx_delivered"] = True
    #                 self.dump_contacts(contacts)
    #             elif status in ["queued", "sending", "sent"]:
    #                 flag = False
    #     return flag