import secrets
import base64
import time
import hashlib
import hmac

class Totp:
    def __init__(self):
        pass

    def generate_secret_key(self):
        secret_key = base64.b32encode(secrets.token_bytes(20)).decode("utf-8")

        return secret_key
    
    def generate_digits(self, secret_key, time_step = None):
        secret_key = base64.b32decode(secret_key)

        if time_step is None:
            time_step = (int(time.time()) // 30).to_bytes(8, "big")
        else:
            time_step = (int(time_step)).to_bytes(8, "big")

        hash_hmac_digest = hmac.new(secret_key, time_step, hashlib.sha1).digest()

        offset = hash_hmac_digest[-1] & 0X0F
        part = hash_hmac_digest[offset:offset + 4]
        truncated = int.from_bytes(part, "big") & 0x7FFFFFFF

        code = truncated % 1000000
        return str(code).zfill(6)

    def verify_digits(self, secret_key, input_code, stretch_ratio = 1):
        current_step = int(time.time()) // 30

        for stretch in range(-stretch_ratio, stretch_ratio + 1):
            if self.generate_digits(secret_key, current_step + stretch) == input_code:
                return True
            
        return False