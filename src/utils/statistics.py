import json
from logging_config import logger as logging
from pprint import pprint, pformat
import datetime

# datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def prepare_statistics_report(result_json_path: str):
    with open(result_json_path, "r") as f:
        contacts = json.load(f)


    result = {
        "contacts_total": len(contacts),

        "contacts_sms_sent": 0,
        "contacts_sms_not_sent": 0,

        "telnyx_sent": 0,
        "twilio_sent": 0,
        "ghl_sent": 0,

        "telnyx_failed": 0,
        "twilio_failed": 0,
        "ghl_failed": 0,

        "date_time": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

    logging.info(f"{prepare_statistics_report.__name__} -- PREPARING SMS OUTREACH STATS FOR - {result['contacts_total']} - CONTACTS")


    for i, contact in enumerate(contacts, start=1):

        logging.info(f"{prepare_statistics_report.__name__} -- CONTACT # - {i}")

        if contact.get("sms_delivered") == True:
            result["contacts_sms_sent"] += 1

        if contact.get("sms_delivered") == False:
            result["contacts_sms_not_sent"] += 1

        if contact.get("telnyx_status") == True:
            result["telnyx_sent"] += 1

        if contact.get("twilio_status") == True:
            result["twilio_sent"] += 1

        if contact.get("ghl_status") == True:
            result["ghl_sent"] += 1

        if contact.get("telnyx_status") == False:
            result["telnyx_failed"] += 1

        if contact.get("twilio_status") == False:
            result["twilio_failed"] += 1

        if contact.get("ghl_status") == False:
            result["ghl_failed"] += 1

    with open("data/outreach_statistics.json", "r") as f:
        statistics_array: list = json.load(f)
        statistics_array.append(result)

    with open("data/outreach_statistics.json", "w") as f:
        json.dump(statistics_array, f)

    logging.info(f"{prepare_statistics_report.__name__} -- STATISTICS PREPARED - {pformat(result)}")

    return result


if __name__ == "__main__":
    prepare_statistics_report("data/updated_contacts.json")

        



