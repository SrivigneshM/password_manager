from app import app


def test_signup(create_actor_table):
    client = app.test_client()
    form_data = dict(
        name="tester",
        email="tester@pwdmgr.com",
        mobile="1234567890",
        password="abc123$%^",
    )
    resp = client.post("/signup", data=form_data)
    assert resp.status_code == 200
    assert resp.data == b"Successfully signed up: tester!"
