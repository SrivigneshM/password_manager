import json
from pathlib import Path

from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

from utils.crypto import AESCipher, license_valid


def test_crypto_functions_decrypt_later():
    password = "tester@1234"
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    iv = get_random_bytes(16)

    raw = "ABDCD##@secret@1234%^&"
    aes_cipher = AESCipher(key)
    cipher_text = aes_cipher.encrypt(raw, iv)

    aes_cipher_new = AESCipher(key)
    plain_text = aes_cipher_new.decrypt(cipher_text, iv)
    assert raw == plain_text


def test_kdf_idempotent():
    password = "tester@1234"
    salt = get_random_bytes(16)
    key1 = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    key2 = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)

    assert key1 == key2


def test_crypto_profile(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="cryptobank",
        user_id="test_id",
        user_name="tester",
        password="abc123$%^",
        password_expiry="2025-01-01",
        crn="234",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.post("/add_profile", data=form_data)
    assert resp.status_code == 200

    form_data = dict(
        app_name="cryptobank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("password") == "abc123$%^"


def test_profile_pwd_update(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="cryptobank",
        user_id="test_id",
        user_name="tester",
        password="abc123$%^",
        password_expiry="2025-01-01",
        crn="234",
        profile_password="secret)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.put("/add_profile", data=form_data)
    assert resp.status_code == 200

    form_data = dict(
        app_name="cryptobank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("password") == "abc123$%^"
    assert profile.get("profile_password") == "secret)(87"


def test_license_valid():
    valid_crt_file = Path(__file__).parent / "valid.p12"
    assert license_valid(valid_crt_file, "test123")
