import json
import time
import requests
from pprint import pprint
from src.logs.logging_config import logger


with open("auth/.ghl_tokens.json", "r") as file:
    keys = json.load(file)


API_KEY = keys["api_key"]
LOCATION_ID = keys["location_id"]
ACCESS_TOKEN = keys["access_token"]
REFRESH_TOKEN = keys["refresh_token"]


def get_conversations(ghl_contact_id):
    """
    searches for Conversations by Contact ID and returns an Conversation object
    """
    logger.info(f"{get_conversations.__name__} -- GHL - GETTING CONVERSATION FOR - {ghl_contact_id}")

    response = requests.get(
        url=f"https://services.leadconnectorhq.com/conversations/search?contactId={ghl_contact_id}",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": "2021-07-28"
        }
    )


    status_code = response.status_code
    logger.info(f"{get_conversations.__name__} -- GHL - STATUS CODE -- {status_code}")

    result = {
        "success": False,
        "data": None,
        "conversation_id": None
    }

    try:
        response_data = response.json()
        logger.info(f"{get_conversations.__name__} -- GHL RESPONSE - {response_data}")

        if response_data["total"] > 0:

            result["success"] = True
            result["data"] = response_data
            result["conversation_id"] = response_data["conversations"][0]["id"]
    except Exception as ex:
        logger.error(f"{get_conversations.__name__} -- !!! GHL ERROR - {ex}")

    return result


def create_conversation(ghl_contact_id):
    """
    creates conversation for a provided Contact ID
    """
    logger.info(f"{create_conversation.__name__} -- GHL - CREATING CONVERSATION FOR - {ghl_contact_id}")

    response = requests.post(
        url=f"https://services.leadconnectorhq.com/conversations/",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": "2021-07-28"
        },
        json={
            "locationId": f"{LOCATION_ID}",
            "contactId": f"{ghl_contact_id}"
        }
    )

    status_code = response.status_code
    logger.info(f"{create_conversation.__name__} -- GHL - STATUS CODE -- {status_code}")

    result = {
        "success": False,
        "data": None,
        "conversation_id": None
    }

    try:
        response_data = response.json()
        logger.info(f"{create_conversation.__name__} -- GHL RESPONSE - {response_data}")

        result["success"] = True if status_code in (201, 200) and response_data["success"] is True else False
        result["data"] = response_data
        result["conversation_id"] = response_data["conversation"]["id"]
    except Exception as ex:
        logger.error(f"{create_conversation.__name__} -- !!! GHL ERROR - {ex}")

    return result


def add_inbound_message(ghl_conversation_id, message_text):
    """
    creates inbound Message in a Conversation for a provided Contact ID
    """
    logger.info(f"{add_inbound_message.__name__} -- GHL - ADDING SMS NOTE TO -- {ghl_conversation_id}")
    response = requests.post(
        url=f"https://services.leadconnectorhq.com/conversations/messages/inbound",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": "2021-07-28"
        },
        json={
            "type": "SMS",
            "conversationId": f"{ghl_conversation_id}",
            "message": f"{message_text}",
            "direction": "inbound"
        }
    )

    status_code = response.status_code
    logger.info(f"{add_inbound_message.__name__} -- GHL - STATUS CODE -- {status_code}")

    result = False

    try:
        response_data = response.json()
        logger.info(f"{add_inbound_message.__name__} -- GHL RESPONSE - {response_data}")

        result = True if response_data["success"] is True else False
    except Exception as ex:
        logger.error(f"{add_inbound_message.__name__} -- !!! GHL ERROR - {ex}")

    return result


# def add_inbound_message(ghl_conversation_id, message_text):
#     """
#     creates inbound Message in a Conversation for a provided Contact ID
#     """
#     logger.info(f"{add_outbound_message.__name__} -- GHL - ADDING SMS NOTE TO -- {ghl_conversation_id}")
#     response = requests.post(
#         url=f"https://services.leadconnectorhq.com/conversations/messages/outbound",
#         headers={
#             "Authorization": f"Bearer {ACCESS_TOKEN}",
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#             "Version": "2021-07-28"
#         },
#         json={
#             "type": "SMS",
#             "conversationId": f"{ghl_conversation_id}",
#             "message": f"{message_text}",
#             "direction": "outbound"
#         }
#     )

#     status_code = response.status_code
#     logger.info(f"{add_outbound_message.__name__} -- GHL - STATUS CODE -- {status_code}")

#     result = False

#     try:
#         response_data = response.json()
#         logger.info(f"{add_outbound_message.__name__} -- GHL RESPONSE - {response_data}")

#         result = True if response_data["success"] is True else False
#     except Exception as ex:
#         logger.error(f"{add_outbound_message.__name__} -- !!! GHL ERROR - {ex}")

#     return result


def set_ghl_sms_blast_status(contact_id: str, status: str):
    """
    sets SMS sent result status for provided Contact ID
    """
    BASE_URL = f"https://services.leadconnectorhq.com/contacts/{contact_id}/"
    HEADERS = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Version': '2021-07-28'
    }
    PAYLOAD = {
        "customFields": [
        {
            "id": "KdiQPtxUnTXWEP4k0PW9",
            "value": status # success / failed
        },
        {
            "id": "t51MQqbEKlCera44Wgmw",
            "value": 1 if status.lower() == "success" else 0
        }
            ]
                }
    logger.info(f"{set_ghl_sms_blast_status.__name__} -- GHL - SETTING STATUS - {status} FOR - {contact_id}")

    response = requests.put(
        url=BASE_URL, headers=HEADERS,
        json=PAYLOAD
    )

    status_code = response.status_code
    logger.info(f"{set_ghl_sms_blast_status.__name__} -- GHL - STATUS CODE -- {status_code}")

    result = False

    try:
        response_data = response.json()
        logger.info(f"{set_ghl_sms_blast_status.__name__} -- GHL RESPONSE - {response_data}")

        result = True if response_data["succeded"] is True else False
    except Exception as ex:
        logger.error(f"{set_ghl_sms_blast_status.__name__} -- !!! GHL ERROR - {ex}")

    return result


def modify_ghl_conversation(contact_id, sms_message):
    """
    handles Conversation modification for a provided Contact ID
    by defining whether provided Contact has a Conversation
    """

    logger.info(f"{modify_ghl_conversation.__name__} -- MODIFYING CONTACTs CONVERSATIONS - {contact_id}")

    get_conversation_response = get_conversations(contact_id)
    time.sleep(0.1)

    if get_conversation_response["success"] is True:
        conversation_id = get_conversation_response["conversation_id"]

        return True if add_inbound_message(conversation_id, sms_message) is True else False
    
    else:
        create_conversation_response = create_conversation(contact_id)
        time.sleep(0.1)

        if create_conversation_response["success"] is True:
            conversation_id = create_conversation_response["conversation_id"]

            return True if add_inbound_message(conversation_id, sms_message) is True else False


def delete_conversation(conversation_id: str):
    """
    deletes Conversation by proving it's ID
    """
    BASE_URL = f"https://services.leadconnectorhq.com/conversations/{conversation_id}"
    HEADERS = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Version': '2021-04-15'
    }
    response = requests.delete(url=BASE_URL, headers=HEADERS)

    status_code = response.status_code
    data_json = response.json()

    result = {
        "status_code": status_code,
        "data": data_json
    }

    logger.info(f"\n{delete_conversation.__name__} -- GHL RESPONSE - {result}")
    return result


def send_sms_ghl(contact_id: str, message: str):
    """
    sends single SMS message with GHL
    """
    BASE_URL = f"https://services.leadconnectorhq.com/conversations/messages"
    HEADERS = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Version': '2021-04-15'
    }
    PAYLOAD = {
        "type": "SMS",
        "contactId": contact_id,
        "message": message
    }
    response = requests.post(url=BASE_URL, headers=HEADERS, json=PAYLOAD)
    
    status_code = response.status_code
    logger.info(f"{send_sms_ghl.__name__} -- GHL - STATUS CODE -- {status_code}")

    result = False

    try:
        response_data = response.json()
        logger.info(f"{send_sms_ghl.__name__} -- GHL RESPONSE - {response_data}")

        result = True if status_code in (201, 200) else False
    except Exception as ex:
        logger.error(f"{send_sms_ghl.__name__} -- !!! GHL ERROR - {ex}")

    return result


def get_ghl_contacts():
    BASE_URL = "https://rest.gohighlevel.com/v1/contacts/?limit=20"
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
    }
    response = requests.get(url=BASE_URL, headers=HEADERS)
    data_json = response.json()
    status_code = response.status_code

    result = {
        "status_code": status_code,
        "data": data_json
    }

    logger.info(f"{get_ghl_contacts.__name__} -- GHL RESPONSE - {result}")

    return result



if __name__ == "__main__":
    
    # conversations = get_conversations("4jGvEwBIInorbmHszdyF")

    # create_conversation("4jGvEwBIInorbmHszdyF")
# 
    add_inbound_message("Y4ouF1FodLLR2OU2uitm", "Test Message")





        


