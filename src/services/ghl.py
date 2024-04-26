import json
# 1) Load json of contacts to a var
# 2) Take a contact → check if “ghl_sent” == False → sent sms →
#set ghl_sent = True, set “ghl_sent_at” = datetime.now(utc)→ save changes to json
# 3) Sending ended → initialize delivery checking

    # [{"message": "",
    # "telnyx_sent": false,
    # "telnyx_delivered": false,
    # "telnyx_message_id": "null",
    # "twilio_sent": false,
    # "twilio_delivered": false,
    # "twilio_message_id": false,
    # "ghl_sent": false,
    # "ghl_delivered": false,
    # "sms_delivered": false,
    # "sms_sent_at": "null"}]


def json_processor(input_file):
    with open(input_file) as f:
        data = json.load(f)
    return data


def update_json(output_file, data):
    with open(output_file) as f:
        json.dump(f, data, indent=4)


def check_field_status(contact, field):
    pass


def update_field_status(contact, field):
    pass


def set_contact_status(contact):
    pass


def send_sms(contact):
    pass


def sms_process(contact):
    ghl_sent_status = check_field_status(contact, "ghl_sent")
    if not ghl_sent_status:
        send_sms(contact)
        update_field_status(contact, "ghl_sent")
        update_field_status(contact, "updated_at")

# 4) Take a contact → check if “ghl_sent” == True → check if sms dellivered →
#set ghl_delivered = True → save changes to json
# 5) Delivery checking ended
# 6) Take a contact → check a ”ghl_delivered” == True →
#get request to ghl (check if contact has conversation)
def delivery_process(contact):
    ghl_sent_status = check_field_status(contact, "ghl_sent")
    ghl_delivery_status = check_field_status(contact, "delivery_status")
    if ghl_sent_status:
        if not ghl_delivery_status:
            update_field_status(contact, "ghl_delivered")
            update_field_status(contact, "updated_at")


def get_ghl():
    pass


def main(input_file, output_file):
    data = json_processor(input_file)
    for i, contact in data:
        sms_process(contact)
        delivery_process(contact)