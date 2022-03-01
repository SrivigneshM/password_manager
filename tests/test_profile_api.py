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
        app_name="swissbank",
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
    assert resp.data == b"Unable to add details for: swissbank!"


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
