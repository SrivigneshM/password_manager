import json


def test_create_profile(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="swissbank",
        user_id="test_id",
        user_name="tester",
        password="secret12#$",
        password_expiry="2025-01-01",
        crn="234",
        profile_password="secret)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.post("/add_profile", data=form_data)
    assert resp.status_code == 200
    assert resp.data == b"Successfully added details for: swissbank!"


def test_create_profile_failure(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="scotlandbank",
        user_id="test_id",
        user_name="tester",
        # password is a mandatory field
        crn="234",
        profile_password="secret)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.post("/add_profile", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Unable to add details for: scotlandbank!"


def test_create_profile_actor_validation_failure(client, logout_actor, create_profile_table):
    form_data = dict(
        app_name="swissbank",
        user_id="test_id",
        user_name="tester",
        password="secret12#$",
        password_expiry="2025-01-01",
        crn="234",
        profile_password="secret)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.post("/add_profile", data=form_data)
    assert resp.status_code == 302


def test_create_profile_app_validation_failure(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="swissbank",
        user_id="test_id",
        user_name="tester",
        password="secret12#$",
        password_expiry="2025-01-01",
        crn="234",
        profile_password="secret)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
    )
    resp = client.post("/add_profile", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Application name is already present: swissbank!"


def test_read_profile(client, login_actor, create_profile_table):
    form_data = dict(
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("user_id") == "test_id"
    assert profile.get("url") == "https://swissb.com"
    assert profile.get("password_iv") is not None
    assert profile.get("profile_password_iv") is not None


def test_read_profile_actor_validation_failure(client, logout_actor, create_profile_table):
    form_data = dict(
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    assert resp.status_code == 302


def test_update_profile(client, login_actor, create_profile_table):
    form_data = dict(
        user_id="test_id",
        user_name="tester",
        password="terces12#$",
        password_expiry="2025-01-01",
        crn="234",
        profile_password="terces)(87",
        url="https://swissb.com",
        is_active=True,
        customer_care_number="0800231-2141-2115",
        remarks="Account details are saved in the secret vault",
        app_name="swissbank",
    )
    resp = client.put("/add_profile", data=form_data)
    assert resp.status_code == 200
    assert resp.data == b"Successfully updated details for: swissbank!"

    form_data = dict(
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("password") == "terces12#$"
    assert profile.get("profile_password") == "terces)(87"


def test_update_profile_failure(client, login_actor, create_profile_table):
    form_data = dict(
        user_id="test_id",
        crn=234,
        app_name="swissbank",
    )
    resp = client.put("/add_profile", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Unable to update details for: swissbank!"


def test_get_apps_list(client, login_actor, create_profile_table):
    resp = client.get("/get_apps_list")
    payload = json.loads(resp.data)
    assert resp.status_code == 200
    assert "swissbank" in payload.get("apps_list")
