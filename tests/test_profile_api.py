import json

from app import app


def test_create_profile(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
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


def test_create_profile_failure(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
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


def test_create_profile_actor_validation_failure(create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="hacker",
        actor_password="abc123$%^",
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
    assert resp.data == b"User name or password incorrect/ mismatched!"


def test_create_profile_app_validation_failure(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
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


def test_read_profile(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("user_id") == "test_id"
    assert profile.get("url") == "https://swissb.com"


def test_read_profile_actor_validation_failure(create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="hacker",
        actor_password="abc123$%^",
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 400
    assert profile.get("message") == "User name or password incorrect/ mismatched!"


def test_update_profile(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
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
        actor_name="tester",
        actor_password="abc123$%^",
        app_name="swissbank",
    )
    resp = client.post("/read_profile", data=form_data)
    profile = json.loads(resp.data)
    assert resp.status_code == 200
    assert profile.get("password") == "terces12#$"
    assert profile.get("profile_password") == "terces)(87"


def test_update_profile_failure(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
        user_id="test_id",
        crn=234,
        app_name="swissbank",
    )
    resp = client.put("/add_profile", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Unable to update details for: swissbank!"


def test_get_apps_list(create_actor, create_profile_table):
    client = app.test_client()
    form_data = dict(
        actor_name="tester",
        actor_password="abc123$%^",
    )
    resp = client.post("/get_apps_list", data=form_data)
    payload = json.loads(resp.data)
    assert resp.status_code == 200
    assert payload.get("apps_list") == ["swissbank"]
