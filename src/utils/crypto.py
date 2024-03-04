import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.serialization import pkcs12

kdict = dict()


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw, iv):
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(raw.encode(), 16))
        return ct

    def decrypt(self, enc, iv):
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(enc), 16)
        return pt.decode()


def load_user(actor_id, key):
    if actor_id not in kdict:
        kdict[actor_id] = AESCipher(key)


def unload_user(actor_id):
    kdict.pop(actor_id, None)


def get_instance(actor_id):
    return kdict.get(actor_id, None)


def license_valid(license_file, passwd):
    valid = True
    try:
        pvt_key, crt, addnl_crt = pkcs12.load_key_and_certificates(
            open(license_file, "rb").read(), passwd.encode("UTF-8")
        )
        expiry = crt.not_valid_after_utc.strftime("%Y%m%d%H%M%SZ")
        now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%SZ")
        if expiry < now:
            valid = False
    except Exception:
        valid = False
    return valid
