import json
import time
from src.logs.logging_config import logger
import datetime
import src.services.telnyx_api as telnyx
from services.twilio_services import Twilio
import src.services.ghl_api as ghl


def sms_blaster(contacts_json_path: str):
    telnyx_sent_contacts = []
    telnyx_from_numbers = ["+19172031916", "+19172031898", "+19172031897"]

    twilio_sent_contacts = []
    ghl_sent_contacts = []

    telnyx_delivered_contacts = []
    twilio_delivered_contacts = []

    # retrieving contacts
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    logger.info(f"{sms_blaster.__name__} -- {len(contacts)} CONTACTS RECEIVED")
    logger.info(f"{sms_blaster.__name__} -- STARTING TELNYX SENDING")

    # 1. Telnyx sending
    for i, contact in enumerate(contacts, start=1):
        sms_message = ("Hi)!\nThis is Bill, "
                       "Director of Business Lending at CAPLOA. We can get you "
                       "approved within one hour for Capital for your business "
                       "and get the money in your bank today!\n\nInterested Just Respond YES\n")

        to_phone_number = str(contact.get("Phone", ""))
        contact_name = contact.get("First Name")

        telnyx_from_numbers.append(telnyx_from_numbers.pop(0))

        # telnyx_from_numbers = ["+19172031883", "+19172031874", "+19172031872"]

        logger.info(f"--\n\n")
        logger.info(f"{sms_blaster.__name__} ** TELNYX SENDING\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT N - {i}\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")

        # if i < 20:
        #     input(">> ")

        # skipping Telnyx sent contacts
        if contact.get("sms_delivered") is True or contact.get("telnyx_sent") is True or contact.get("telnyx_delivered") is True:
            logger.info(f"{sms_blaster.__name__} -- SKIPPING CONTACT")
            continue

        # formatting sms message
        if contact_name:
            sms_message = sms_message.replace(")", f", {contact_name}")
        else:
            sms_message = sms_message.replace(")", "")

        logger.info(f"{sms_blaster.__name__} -- SMS MESSAGE - {sms_message}")
        contact["message"] = sms_message

        if to_phone_number not in telnyx_sent_contacts:

            # sending SMS with Telnyx
            telnyx_sent_result = telnyx.send_telnyx_sms(to_phone_number,
                                                        sms_message,
                                                        telnyx_from_numbers[0])
            # telnyx_sent_result = {"success": False}

            if telnyx_sent_result["success"] is True:
                logger.info(f"{sms_blaster.__name__} -- TELNYX - SMS SENT SUCCESSFULLY FOR - {to_phone_number}")

                contact["telnyx_sent"] = True
                contact["telnyx_message_id"] = telnyx_sent_result["message_id"]

                telnyx_sent_contacts.append(to_phone_number)
            else:
                logger.warning(f"{sms_blaster.__name__} -- ! TELNYX - SMS NOT SENT - {to_phone_number}")

        else:
            contact["telnyx_sent"] = True
            # contact["telnyx_message_id"] = telnyx_sent_result["message_id"]
        # dumping updated contacts on each iteration
        with open(contacts_json_path, "w") as f:
            json.dump(contacts, f, indent=4)
        time.sleep(1)

    logger.info(f"{sms_blaster.__name__} -- FINISHED TELNYX SENDING\n\n")
    # Telnyx Sending finished -----------------------------------------------------------------------------------------------------
    time.sleep(10)
    # input(">>")
    # Telnyx delivery status checking started -------------------------------------------------------------------------------------
    logger.info(f"{sms_blaster.__name__} -- STARTING TELNYX DELIVERY CHECKING")
    # retrieving contacts
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)
    # 2. Telnyx delivery checking
    for i, contact in enumerate(contacts, start=1):
        logger.info(f"--\n\n")
        logger.info(f"{sms_blaster.__name__} ** TELNYX DELIVERY CHECKING\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT N - {i}\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")

        if contact.get("sms_delivered") is True or contact.get("telnyx_sent") != True:
            logger.info(f"{sms_blaster.__name__} -- SKIPPING CONTACT")
            continue

        contact_id = contact.get("Contact Id")
        to_phone_number = str(contact.get("Phone", ""))
        message_id = contact.get("telnyx_message_id")
        message = contact.get("message")

        if to_phone_number not in telnyx_delivered_contacts:

            # checking Telnyx delivery status
            telnyx_delivery_result = telnyx.check_telnyx_delivery_status(message_id)

            if telnyx_delivery_result is True:
                logger.info(f"{sms_blaster.__name__} -- TELNYX - SMS DELIVERED SUCCESSFULLY FOR - {to_phone_number}")

                contact["telnyx_delivered"] = True
                contact["sms_delivered"] = True
                contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                telnyx_delivered_contacts.append(to_phone_number)

                # Updating contact info in GHL
                ghl_modification_response = ghl.modify_ghl_conversation(contact_id, message)

                if ghl_modification_response is True:
                    logger.info(f"{sms_blaster.__name__} -- GHL - SMS NOTE SUCCESSFULLY ADDED TO - {contact_id}")

                    # Setting GHL SMS sending Status
                    ghl_status_setting_response = False

                    # try:
                    #     ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
                    # except Exception as ex:
                    #     logging.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

                    if ghl_status_setting_response is True:
                            logger.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")
            else:
                logger.warning(f"{sms_blaster.__name__} -- ! TELNYX - SMS NOT DELIVERED - {to_phone_number}")
        else:
            contact["telnyx_delivered"] = True
            contact["sms_delivered"] = True
            contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            telnyx_delivered_contacts.append(to_phone_number)
            # Updating contact info in GHL
            ghl_modification_response = ghl.modify_ghl_conversation(contact_id, message)

            if ghl_modification_response is True:
                logger.info(f"{sms_blaster.__name__} -- GHL - SMS NOTE SUCCESSFULLY ADDED TO - {contact_id}")
                # Setting GHL SMS sending Status
                ghl_status_setting_response = False

                # try:
                    # ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
                # except Exception as ex:
                #     logging.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

                if ghl_status_setting_response is True:
                        logger.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")

        # dumping updated contacts on each iteration
        with open(contacts_json_path, "w") as f:
            json.dump(contacts, f, indent=4)

        time.sleep(0.1)

    logger.info(f"{sms_blaster.__name__} -- FINISHED TELNYX DELIVERY CHECKING\n\n")
    # telnyx processing finished =========================================================================================================

    time.sleep(10)
    # input(">>")

    # twilio processing started ==========================================================================================================
    
    # retrieving contacts
    # with open(contacts_json_path, "r") as f:
    #     contacts = json.load(f)

    # logging.info(f"{sms_blaster.__name__} -- STARTING TWILIO SENDING")

    # # 3. Twilio sending
    # for i, contact in enumerate(contacts, start=1):

    #     sms_message = "Hello),\n\nI'm Adam Shapiro from Military & Patriots Investment Group, and I'm excited to share another compelling Self-Storage opportunity—a development in San Antonio, Texas, by Argus. This asset offers a potential 21+% IRR and 57%+ ROI, spanning over 80,000 sq ft with 700+ climate-controlled units. The project provides an excellent exit opportunity in just 2 years with institutional quality buyers.\n\nWith our proven track record of 200+ ground-up projects, most being successful 2-year holds, it's an opportunity worth exploring.\n\nInterested? Reply 'Yes.'\n\nBest\nAdam Shapiro\n\nNot interested? Reply 'OUT' to opt out."

    #     logging.info(f"--\n\n")
    #     logging.info(f"{sms_blaster.__name__} ** TWILIO SENDING\n")
    #     logging.info(f"{sms_blaster.__name__} -- CONTACT N - {i}\n")
    #     logging.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")


    #     # skipping Twilio sent contacts  
    #     if contact.get("sms_delivered") is True or contact.get("twilio_sent") is True or contact.get("twilio_delivered") is True:
    #         logging.info(f"{sms_blaster.__name__} -- SKIPPING CONTACT")
    #         continue
            

    #     to_phone_number = str(contact.get("Phone", ""))
    #     contact_name = contact.get("First Name")

    #     # formatting sms message
    #     if contact_name:
    #         sms_message = sms_message.replace(")", f" {contact_name}")
    #     else:
    #         sms_message = sms_message.replace(")", "")
        
    #     logging.info(f"{sms_blaster.__name__} -- SMS MESSAGE - {sms_message}")

    #     contact["message"] = sms_message

    #     if to_phone_number not in twilio_sent_contacts:

    #         # sending SMS with Twilio
    #         twilio = Twilio()
    #         twilio_sent_result = twilio.send_sms(to_phone_number, sms_message)

    #         if twilio_sent_result["success"] is True:
    #             logging.info(f"{sms_blaster.__name__} -- TWILIO - SMS SENT SUCCESSFULLY FOR - {to_phone_number}")

    #             contact["twilio_sent"] = True
    #             contact["twilio_message_id"] = twilio_sent_result["sms_id"]

    #             twilio_sent_contacts.append(to_phone_number)
    #         else:
    #             logging.warning(f"{sms_blaster.__name__} -- ! TWILIO - SMS NOT SENT - {to_phone_number}")

    #     else:
    #         contact["twilio_sent"] = True
    #         # contact["twilio_message_id"] = twilio_sent_result["message_id"]

    #     # dumping updated contacts on each iteration
    #     with open(contacts_json_path, "w") as f:
    #         json.dump(contacts, f)

    #     time.sleep(0.1)

    # logging.info(f"{sms_blaster.__name__} -- FINISHED TWILIO SENDING\n\n")
    # # Twilio Sending finished -----------------------------------------------------------------------------------------------------

    # time.sleep(10)
    # # input(">>")


    # # Twilio delivery status checking started -------------------------------------------------------------------------------------
    # logging.info(f"{sms_blaster.__name__} -- STARTING TWILIO DELIVERY CHECKING")

    # # retrieving contacts
    # with open(contacts_json_path, "r") as f:
    #     contacts = json.load(f)

    # # 4. Twilio delivery checking
    # for i, contact in enumerate(contacts, start=1):

    #     logging.info(f"--\n\n")
    #     logging.info(f"{sms_blaster.__name__} ** TWILIO DELIVERY CHECKING\n")
    #     logging.info(f"{sms_blaster.__name__} -- CONTACT N - {i}\n")
    #     logging.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")


    #     if contact.get("sms_delivered") is True or contact.get("twilio_sent") != True:
    #         logging.info(f"{sms_blaster.__name__} -- SKIPPING CONTACT")
    #         continue

    #     contact_id = contact.get("Contact Id")
    #     to_phone_number = str(contact.get("Phone", ""))
    #     message_id = contact.get("twilio_message_id")
    #     message = contact.get("message")

    #     if to_phone_number not in twilio_delivered_contacts:

    #         # checking Twilio delivery status
    #         twilio = Twilio()
    #         twilio_delivery_result = twilio.sms_status(message_id)

    #         if twilio_delivery_result is True:
    #             logging.info(f"{sms_blaster.__name__} -- TWILIO - SMS DELIVERED SUCCESSFULLY FOR - {to_phone_number}")

    #             contact["twilio_delivered"] = True
    #             contact["sms_delivered"] = True
    #             contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    #             twilio_delivered_contacts.append(to_phone_number)

    #             # Updating contact info in GHL
    #             ghl_modification_response = ghl.modify_ghl_conversation(contact_id, message)

    #             if ghl_modification_response is True:
    #                 logging.info(f"{sms_blaster.__name__} -- GHL - SMS NOTE SUCCESSFULLy ADDED TO - {contact_id}")

    #                 # Setting GHL SMS sending Status
    #                 ghl_status_setting_response = False

    #                 try:
    #                     ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
    #                 except Exception as ex:
    #                     logging.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

    #                 if ghl_status_setting_response is True:
    #                         logging.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")
    #         else:
    #             logging.warning(f"{sms_blaster.__name__} -- ! TWILIO - SMS NOT DELIVERED - {to_phone_number}")

    #     else:
    #         contact["twilio_delivered"] = True
    #         contact["sms_delivered"] = True
    #         contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    #         twilio_delivered_contacts.append(to_phone_number)

    #         # Updating contact info in GHL
    #         ghl_modification_response = ghl.modify_ghl_conversation(contact_id, message)

    #         if ghl_modification_response is True:
    #             logging.info(f"{sms_blaster.__name__} -- GHL - SMS NOTE SUCCESSFULLY ADDED TO - {contact_id}")

    #             # Setting GHL SMS sending Status
    #             ghl_status_setting_response = False

    #             try:
    #                 ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
    #             except Exception as ex:
    #                 logging.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

    #             if ghl_status_setting_response is True:
    #                     logging.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")

    #     # dumping updated contacts on each iteration
    #     with open(contacts_json_path, "w") as f:
    #         json.dump(contacts, f)

    #     time.sleep(0.1)

    # logging.info(f"{sms_blaster.__name__} -- FINISHED TWILIO DELIVERY CHECKING\n\n")
    # # twilio processing finished =========================================================================================================

    # time.sleep(10)
    # # input(">>")
                
    # # ghl processing started ==========================================================================================================
    
    # retrieving contacts
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    logger.info(f"{sms_blaster.__name__} -- STARTING GHL SENDING")

    # 5. GHL sending
    for i, contact in enumerate(contacts, start=1):

        sms_message = "Hello),\n\nI'm Adam Shapiro from Military & Patriots Investment Group, and I'm excited to share another compelling Self-Storage opportunity—a development in San Antonio, Texas, by Argus. This asset offers a potential 21+% IRR and 57%+ ROI, spanning over 80,000 sq ft with 700+ climate-controlled units. The project provides an excellent exit opportunity in just 2 years with institutional quality buyers.\n\nWith our proven track record of 200+ ground-up projects, most being successful 2-year holds, it's an opportunity worth exploring.\n\nInterested? Reply 'Yes.'\n\nBest\nAdam Shapiro\n\nNot interested? Reply 'OUT' to opt out."

        logger.info(f"--\n\n")
        logger.info(f"{sms_blaster.__name__} ** GHL SENDING\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT N - {i}\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")


        # skipping GHL sent contacts  
        if contact.get("sms_delivered") is True or contact.get("ghl_sent") is True or contact.get("ghl_delivered") is True:
            logger.info(f"{sms_blaster.__name__} -- SKIPPING CONTACT")
            continue
            

        contact_id = contact.get("Contact Id")
        contact_name = contact.get("First Name")

        # formatting sms message
        if contact_name:
            sms_message = sms_message.replace(")", f" {contact_name}")
        else:
            sms_message = sms_message.replace(")", "")
        
        logger.info(f"{sms_blaster.__name__} -- SMS MESSAGE - {sms_message}")

        contact["message"] = sms_message

        if contact_id not in ghl_sent_contacts:

            # sending SMS with GHL
            ghl_sending_response = ghl.send_sms_ghl(contact_id, sms_message)

            if ghl_sending_response is True:
                logger.info(f"{sms_blaster.__name__} -- GHL - SMS SENT SUCCESSFULLY FOR - {contact_id}")

                contact["ghl_sent"] = True
                contact["ghl_delivered"] = True
                contact["sms_delivered"] = True
                contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                ghl_sent_contacts.append(contact_id)

                # Setting GHL SMS sending Status
                ghl_status_setting_response = False

                try:
                    ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
                except Exception as ex:
                    logger.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

                if ghl_status_setting_response is True:
                        logger.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")

            else:
                logger.warning(f"{sms_blaster.__name__} -- ! GHL - SMS NOT SENT - {to_phone_number}")

        else:
            contact["ghl_sent"] = True
            contact["ghl_delivered"] = True
            contact["sms_delivered"] = True
            contact["sms_sent_at"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            ghl_sent_contacts.append(contact_id)

            # Setting GHL SMS sending Status
            ghl_status_setting_response = False

            try:
                ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Success")
            except Exception as ex:
                logger.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

            if ghl_status_setting_response is True:
                    logger.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")

        # dumping updated contacts on each iteration
        with open(contacts_json_path, "w") as f:
            json.dump(contacts, f)

        time.sleep(0.1)

    logger.info(f"{sms_blaster.__name__} -- FINISHED GHL SENDING\n\n")
    # # GHL Sending finished -----------------------------------------------------------------------------------------------------
    # # GHL processing finished ==================================================================================================

    # time.sleep(5)
    # input(">>")

    # starting marking failed contacts =========================================================================================

    # retrieving contacts
    with open(contacts_json_path, "r") as f:
        contacts = json.load(f)

    logger.info(f"{sms_blaster.__name__} -- STARTING MARKING FAILED CONTACTS STATUSES")

    # 6. Marking failed contacts
    for i, contact in enumerate(contacts, start=1):

        logger.info(f"--\n\n")
        logger.info(f"{sms_blaster.__name__} -- CONTACT N - {i}")
        logger.info(f"{sms_blaster.__name__} ** FAILED CONTACTS MARKING")
        logger.info(f"{sms_blaster.__name__} -- CONTACT DATA - {contact}")

        # if contact.get("sms_delivered") is not True:

        #     contact_id = contact.get("Contact Id")

        #     # Setting GHL SMS sending Status
        #     ghl_status_setting_response = False

        #     try:
        #         ghl_status_setting_response = ghl.set_ghl_sms_blast_status(contact_id, "Failed")
        #     except Exception as ex:
        #         logging.error(f"{sms_blaster.__name__} -- !!!! GHL ERROR - {ex}")

        #     if ghl_status_setting_response is True:
        #             logging.info(f"{sms_blaster.__name__} -- GHL - STATUS SUCCESSFULLY UPDATED - {contact_id}")


    logger.info(f"{sms_blaster.__name__} -- SMS BLASTING COMPLETED ====")
