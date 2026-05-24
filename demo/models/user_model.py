import sqlite3
from config import DB_PATH

class UserModel:
    def __init__(self):
        self.db_path = DB_PATH
        
    def get_connection(self):
        # timeout = db meşgulse bekleme süresi
        return sqlite3.connect(self.db_path, timeout=10)
        
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user
        
    def create_user(self, username, hashed_password):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Bütünlük hatası / kullanıcı zaten var
            return False
        finally:
            conn.close()

    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def save_totp_details(self, user_id, secret, backup_codes_str):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET totp_secret=?, totp_enabled=1 WHERE id=?", (secret, user_id))
            
            cursor.execute("SELECT id FROM totp_backup_keys WHERE user_id=?", (user_id,))
            if cursor.fetchone():
                cursor.execute("UPDATE totp_backup_keys SET backup_codes=?, used_backup_codes='' WHERE user_id=?", (backup_codes_str, user_id))
            else:
                cursor.execute("INSERT INTO totp_backup_keys (user_id, backup_codes, used_backup_codes) VALUES (?, ?, '')", (user_id, backup_codes_str))
                
            conn.commit()
        finally:
            conn.close()

    def disable_totp(self, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET totp_secret=NULL, totp_enabled=0 WHERE id=?", (user_id,))
            cursor.execute("DELETE FROM totp_backup_keys WHERE user_id=?", (user_id,))
            conn.commit()
        finally:
            conn.close()

    def get_backup_codes(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT backup_codes, used_backup_codes FROM totp_backup_keys WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_backup_codes(self, user_id, backup_codes_str, used_backup_codes_str):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE totp_backup_keys SET backup_codes=?, used_backup_codes=? WHERE user_id=?", (backup_codes_str, used_backup_codes_str, user_id))
            conn.commit()
        finally:
            conn.close()
