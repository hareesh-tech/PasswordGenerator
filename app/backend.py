import sqlite3
import hashlib
import secrets
import string
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handles all database operations for password storage"""

    def __init__(self, db_name='Output/pass_fort.db'):
        self.db_name = db_name
        Path("Output").mkdir(exist_ok=True)
        self.init_database()

    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    uid TEXT PRIMARY KEY,
                    hashed_password TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            logger.info(f"Database initialized: {self.db_name}")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def save_password(self, uid, password):
        try:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            timestamp = datetime.now()

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO passwords (uid, hashed_password, timestamp)
                VALUES (?, ?, ?)
            ''', (uid, hashed, timestamp))
            conn.commit()
            conn.close()

            logger.info("="*80)
            logger.info("PASSWORD SAVED")
            logger.info(f"UID: {uid}")
            logger.info(f"SHA-256: {hashed}")
            logger.info("="*80)

            return True
        except Exception as e:
            logger.error(f"Error saving password: {e}")
            return False


class PasswordGenerator:
    """Core password generation engine"""

    @staticmethod
    def generate(length=16, add_symbols=True, only_text=False, only_numbers=False):

        length = max(8, min(64, int(length)))

        letters = string.ascii_letters
        numbers = string.digits
        symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'

        if only_text:
            char_pool = letters
        elif only_numbers:
            char_pool = numbers
        else:
            char_pool = letters + numbers
            if add_symbols:
                char_pool += symbols

        password = ''.join(secrets.choice(char_pool) for _ in range(length))

        logger.info("="*80)
        logger.info("NEW PASSWORD GENERATED")
        logger.info(f"Length: {length}")
        logger.info("="*80)

        return password