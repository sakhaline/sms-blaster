import os
import json
from src import DATADIR
from src.services.telnyx_api import TelnyxApi
from src.services.ghl_api import GHLApi
from src.services.ghl_service import GHLService
from src.services.telnyx_service import TelnyxService
from src.logs.logging_config import logger



TELNYX = TelnyxService()
GHL = GHLService()
GHLAPI = GHLApi()
contacts_file = os.path.join(DATADIR, "contacts.json")


def generate_correct_contacts_json(contacts):
    for contact in contacts:
        contact["message"] = ""
        contact["telnyx_sent"] = False
        contact["telnyx_delivered"] = False
        contact["telnyx_message_id"] = ""
        contact["ghl_sent"] = False
        contact["ghl_delivered"] = False
    with open(contacts_file, "w") as f:
        json.dump(contacts, f, indent=4)


if __name__ == "__main__":
    TELNYX.telnyx_processor()
    # contacts = GHLAPI.get_contact_list()
    # generate_correct_contacts_json(contacts)
