from app import app


def test_signup(create_actor_table):
    client = app.test_client()
    form_data = dict(
        name="newtester",
        email="tester@pwdmgr.com",
        mobile="1234567890",
        password="abc123$%^",
    )
    resp = client.post("/signup", data=form_data)
    assert resp.status_code == 200
    assert resp.data == b"Successfully signed up: newtester!"


def test_signup_failure(create_actor_table):
    client = app.test_client()
    form_data = dict(
        # name is mandatory field
        email="tester@pwdmgr.com",
        mobile="1234567890",
        password="abc123$%^",
    )
    resp = client.post("/signup", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Unable to signup: None!"


def test_signup_duplicate_name(create_actor_table, create_actor):
    client = app.test_client()
    form_data = dict(
        name="tester",
        email="tester@pwdmgr.com",
        mobile="9876543210",
        password="abc123$%^",
    )
    resp = client.post("/signup", data=form_data)
    assert resp.status_code == 400
    assert resp.data == b"Name is already taken: tester!"
