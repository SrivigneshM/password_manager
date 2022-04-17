import datetime

import OpenSSL
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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
        p12 = OpenSSL.crypto.load_pkcs12(open(license_file, "rb").read(), passwd)
        x509 = p12.get_certificate()
        expiry = x509.get_notAfter().decode()
        now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%SZ")
        if expiry < now:
            valid = False
    except Exception:
        valid = False
    return valid
