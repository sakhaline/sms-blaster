import sqlite3
from src.logs.logging_config import logger


class DBAPI:
    def __init__(self):
        self.db_path = "blaster.db"
        self.con = None

    def open_connection(self):
        if self.con is None or self.con.closed:
            self.con = sqlite3.connect(self.db_path)

    def close_connection(self):
        if self.con:
            self.con.close()
            self.con = None

    def create_table(self):
        self.open_connection()
        cursor = self.con.cursor()
        create_table_script = """
        CREATE TABLE Contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ghl_id TEXT NULL,
        fname TEXT NULL,
        lname TEXT NULL,
        phone_number TEXT NULL,
        telnyx_sent INTEGER DEFAULT 0,
        telnyx_delivered INTEGER DEFAULT 0,
        ghl_sent INTEGER DEFAULT 0,
        message TEXT NULL,
        message_id TEXT NULL,
        ghl_conversation_id TEXT NULL,
        ghl_conversation_status INTEGER DEFAULT 1
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            cursor.executescript(create_table_script)
            self.con.commit()
            logger.debug("TABLE CREATED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"FAILED TO CREATE TABLES. ERROR:\n{e}")
        finally:
            self.close_connection()

    def insert_contact(self, ghl_id, fname, lname, phone_number):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        INSERT INTO Contact (ghl_id, fname, lname, phone_number)
        VALUES (?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (ghl_id, fname, lname, phone_number))
            self.con.commit()
            logger.debug(f"CONTACT INSERTED SUCCESSFULLY. ID --> {ghl_id}")

        except sqlite3.Error as e:
            logger.error(f"FAILED TO INSERT CONTACT. ERROR:\n{e}")
        finally:
            self.close_connection()

    def get_ghl_id_by_phone_number(self, phone_number):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        SELECT ghl_id FROM Contact WHERE phone_number = ?
        """
        try:
            cursor.execute(query, (phone_number,))
            result = cursor.fetchone()

            if result:
                ghl_id = result[0]
                logger.debug(f"GHL_ID FOR PHONE {phone_number}: {ghl_id}")
                return ghl_id
            else:
                logger.warning(f"CONTACT WITH PHONE -> {phone_number} <- NOT FOUND")
        except sqlite3.Error as e:
            logger.error(f"FAILED TO GET CONTACT WITH PHONE -> {phone_number} <-. ERROR:\n{e}")
        finally:
            self.close_connection()

    def update_message_by_phone_number(self, phone_number, message_id, message):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        UPDATE Contact
        SET message = ?, message_id = ?
        WHERE phone_number = ?
        """
        try:
            cursor.execute(query, (message, message_id, phone_number))
            self.con.commit()
            logger.debug(f"""MESSAGE -> {message_id} <- TEXT {message}
                         FROM: {phone_number}
                         INSERTED SUCCESSFULLY""")
        except sqlite3.Error as e:
            logger.error(f"FAILED TO INSERT MESSAGE FROM -> {phone_number} <-. ERROR:\n{e}")
        finally:
            self.close_connection()

    def get_phone_number_telnyx_status_list(self, limit):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        SELECT phone_number, telnyx_sent
        FROM Contact
        WHERE telnyx_sent = 0
        LIMIT ?
        """
        try:
            cursor.execute(query, (limit,))
            result = cursor.fetchall()
            logger.debug("PHONE NUMBER LIST FETCHED SUCCESSFULLY")
            return result
        except sqlite3.Error as e:
            logger.error(f"FAILED TO FETCH PHONE NUMBER LIST. ERROR:\n{e}")
            return None
        finally:
            self.close_connection()

    def update_telnyx_sent_sms_id_by_phone_number(self, phone_number, sms_id):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        UPDATE Contact
        SET telnyx_sent = 1, message_id = ?
        WHERE phone_number = ?
        """
        try:
            cursor.execute(query, (sms_id, phone_number))
            self.con.commit()
            logger.debug(f"""TELNYX SMS STATUS, MESSSAGE ID SET SUCCESSFULLY AS 1
                         FOR: {phone_number}""")
        except sqlite3.Error as e:
            logger.error(f"FAILED TO SET TELNYX SMS STATUS FOR -> {phone_number} <-.ERROR:\n{e}")
        finally:
            self.close_connection()

    def update_ghl_conversation_info(self, contact_id, conversation_id, message,
                                     conversation_status=1):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        UPDATE Contact
        SET ghl_conversation_id = ?, message = ?, ghl_sent = 1, ghl_conversation_status = ?
        WHERE ghl_id = ?
        """
        try:
            cursor.execute(query, (conversation_id, message,
                                   conversation_status, contact_id))
            self.con.commit()
            logger.debug(f"""CONTACT WITH ID -> {contact_id} <-
                         UPDATED SUCCESSFULLY WITH CONVERSATION ID -> {conversation_id} <-,
                         WITH MESSAGE TEXT -> {message} <-""")
        except sqlite3.Error as e:
            logger.error(f"""FAILED TO UPDATE CONTACT WITH ID -> {contact_id} <-
                         CONVERSATION ID -> {conversation_id} <-,
                         MESSAGE TEXT -> {message} <-
                         ERROR: {e}""")
        finally:
            self.close_connection()

    def update_ghl_conversation_status(self, conversation_id):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        UPDATE Contact
        SET ghl_conversation_status = 0
        WHERE ghl_conversation_id = ?
        """
        try:
            cursor.execute(query, (conversation_id,))
            self.con.commit()
            logger.debug(f"""CONVERSATION STATUS WITH CONVERSATION ID -> {conversation_id} <- UPDATED TO 0""")
        except sqlite3.Error as e:
            logger.error(f"""FAILED TO UPDATE CONVERSATION STATUS TO #0
                         CONVERSATION ID -> {conversation_id} <-
                         ERROR: {e}""")
        finally:
            self.close_connection()


    def get_message_list(self):
        self.open_connection()
        cursor = self.con.cursor()
        query = """
        SELECT ghl_id, ghl_conversation_id, message FROM Contact
        WHERE message IS NOT NULL
        """
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.debug("PHONE MESSAGE LIST FETCHED SUCCESSFULLY")
            return result
        except sqlite3.Error as e:
            logger.error(f"FAILED TO FETCH MESSAGE LIST. ERROR:\n{e}")
            return None
        finally:
            self.close_connection()
