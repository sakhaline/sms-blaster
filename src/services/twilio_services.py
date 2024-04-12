import os
from dotenv import load_dotenv
from twilio.rest import Client
from logging_config import logger
from utils.utils import format_phone_number

load_dotenv()


class Twilio:
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    def __init__(self):
        self.client = Client(self.TWILIO_SID, self.TWILIO_AUTH_TOKEN)

    def send_sms(self, phone_number, message):
        phone_number = format_phone_number(phone_number)

        logger.info(f"{self.send_sms.__name__} -- TWILIO - SENDING SMS TO - {phone_number}")

        result = {
            "success": None,
            "sms_sid": None
        }

        try:
            sms = self.client.messages.create(
                body=message,
                from_=os.getenv("TWILIO_FROM_NUMBER"),
                to=phone_number
            )
            logger.info(f"{self.send_sms.__name__} -- TWILIO - STATUS - {sms.status}")

            result["success"] = True if sms.status in ("delivered", "queued", "sending", "sent", "receiving", "received", "accepted") else False
            result["sms_id"] = sms.sid

        except Exception:
            logger.error(f"{self.send_sms.__name__} -- !!! TWILIO ERROR")
        
        return result

    def sms_status(self, sid):
        logger.info(f"{self.sms_status.__name__} -- TWILIO - CHECKING DELIVERY STATUS OF - {sid}")
        status = None

        try:
            status = self.client.messages(sid).fetch().status
            # status = self.client.messages(sid).fetch().error_code
            logger.info(f"{self.sms_status.__name__} -- TWILIO - DELIVERY STATUS - {status}")
        except Exception:
            logger.error(f"{self.sms_status.__name__} -- !!! TWILIO ERROR")

        return True if status == "delivered" else False
    

    def __str__(self):
        return "Twillio"

if __name__ == "__main__":
    twilio = Twilio()
    # message = twilio.send_sms('(844) 900-0770', 'test message')
    # print(message)
    # time.sleep(1)
    status = twilio.sms_status("SMf157a5106119ecfd9dbf27af9e6b7228")
    print(status)