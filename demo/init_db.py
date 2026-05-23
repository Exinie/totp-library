import os
import sqlite3


class InitDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def setup(self):
        self._users_table()
        self._totp_backup_keys_table()
        self.conn.commit()
        self.conn.close()

    def _users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                totp_secret TEXT,
                totp_enabled INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    def _totp_backup_keys_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS totp_backup_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                backup_codes TEXT NOT NULL,
                used_backup_codes TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )


def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    InitDB(db_path).setup()
