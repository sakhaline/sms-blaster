import os
from dotenv import load_dotenv
import requests as req

from src.logs.logging_config import logger
import src.utils.utils as utils

load_dotenv()


API_KEY = os.getenv("TELNYX_API_KEY")
PUBLIC_KEY = os.getenv("TELNYX_PUBLIC_KEY")


class TelnyxApi:
    def __init__(self):
        self.url = "https://api.telnyx.com/v2/messages"
        self.headers = {"Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"}
        self.profile_id = "40018fc0-1345-4910-9c4b-07175988d9c9"

    def check_delivery_status(self, message_id: str, delivery_status=None):
        url = f"{self.url}/{message_id}"
        response = req.get(url=url, headers=self.headers)

        if response.status_code == 200:
            delivery_status = response.json()["data"]["to"][-1]["status"]
            logger.info(f"""SUCCESSFULLY CHECKED TELNYX DELIVERY STATUS FOR - {message_id}.
                        STATUS {delivery_status}""")
            return delivery_status
        else:
            logger.error(f"FAIL TO CHECK TELNYX DELIVERY STATUS. ERROR:  {response.text}")


    def send_sms(self, to_number: str, sms_message: str, from_number: str,
                 webhook_url="http://185.69.153.62:5000/"):
        formatted_number = utils.format_phone_number(to_number)
        data = {"type": "SMS",
                "text": f"{sms_message}",
                "from": from_number,
                "to": formatted_number,
                "messaging_profile_id": self.profile_id,
                "webhook_url": webhook_url}
        response = req.post(url=self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            message_id = response.json()["data"]["id"]
            logger.info(f"""SUCCESSFULLY SENT TELNYX MESSAGE TO {formatted_number}.
                        MESSAGE ID: {message_id}""")
            return message_id
        else:
            logger.error(f"""FAIL TO SEND TELNYX MESSAGE. ERROR: {response.text}""")


if __name__ == "__main__":
    pass
