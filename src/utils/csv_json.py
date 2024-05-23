import csv
import json
from logs.logging_config import logger


def convert_csv_to_json(csv_path: str, json_path: str):
    """
    loads data from csv file and stores it into JSON
    output -> list[dict]
    file output -> .json
    """
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["message"] = None

            row["telnyx_sent"] = False
            row["telnyx_delivered"] = False
            row["telnyx_message_id"] = False

            row["twilio_sent"] = False
            row["twilio_delivered"] = False
            row["twilio_message_id"] = False

            row["ghl_sent"] = False
            row["ghl_delivered"] = False

            row["sms_delivered"] = False
            row["sms_sent_at"] = None

            data.append(row)

    with open(json_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)

    logger.info(f"CONVERTED CSV [{csv_path}] TO JSON [{json_path}]")
    return data


if __name__ == "__main__":
    convert_csv_to_json("data/contacts.csv", "data/contacts.json")
