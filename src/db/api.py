import sqlite3
from src.logs.logging_config import logger


class DBAPI:
    def __init__(self):
        self.con = sqlite3.connect('blaster.db')

    def create_table(self):
        try:
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
            ghl_conversation_status INTEGER DEFAULT 0
            );
            """
            cursor.executescript(create_table_script)
            self.con.commit()
            logger.debug("TABLE CREATED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"FAILED TO CREATE TABLES. ERROR:\n{e}")
        finally:
            self.con.close()

    def insert_contact(self, ghl_id, fname, lname, phone_number,
                       telny_sent, telnyx_delivered, ghl_sent,
                       message, message_id, ghl_conversation_id,
                       ghl_conversation_status):
        cursor = self.con.cursor()
        query = """
        INSERT INTO Contact (
            ghl_id, fname, lname, phone_number, telnyx_sent, 
            telnyx_delivered, ghl_sent, message, message_id, 
            ghl_conversation_id, ghl_conversation_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (ghl_id, fname, lname, phone_number,
                                   telny_sent, telnyx_delivered, ghl_sent,
                                   message, message_id, ghl_conversation_id,
                                   ghl_conversation_status))
            self.con.commit()
            logger.debug(f"CONTACT INSERTED SUCCESSFULLY. ID --> {ghl_id}")

        except sqlite3.Error as e:
            logger.error(f"FAILED TO INSERT CONTACT. ERROR:\n{e}")
        finally:
                self.con.close()

    def get_ghl_id_by_phone_number(self, phone_number):
        cursor = self.con.cursor()
        query = """
        SELECT ghl_id FROM Contact WHERE phone_number = ?
        """
        try:
            cursor.execute(query, (phone_number,))
            result = cursor.fetchone()

            if result:
                ghl_id = result[0]
                logger.info(f"GHL_ID FOR PHONE {phone_number}: {ghl_id}")
                return ghl_id
            else:
                logger.warning(f"CONTACT WITH PHONE -> {phone_number} <- NOT FOUND")
        except sqlite3.Error as e:
            logger.error(f"FAILED TO GET CONTACT WITH PHONE -> {phone_number} <-. ERROR:\n{e}")
        finally:
                self.con.close()

    def update_message_by_phone_number(self, phone_number, message_id, message):
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
            self.con.close()

    def get_phone_numbers(self, start, end):
        cursor = self.con.cursor()
        query = """
        SELECT phone_number FROM Contact
        WHERE id BETWEEN ? AND ?
        """