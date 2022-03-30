from pathlib import Path

import pytest

from dao import db_access
from utils.constants import project_root
from webapps.app import app


@pytest.fixture(scope="function")
def mock_db_file(mocker):
    mocker.patch.object(db_access, "db_file", Path(f"{project_root}/test_password_manager.db"))


@pytest.fixture()
def create_actor_table(mock_db_file):
    sql_create_actor_table = """CREATE TABLE IF NOT EXISTS actor(
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   password TEXT NOT NULL,
                                   salt TEXT NOT NULL,
                                   name TEXT NOT NULL,
                                   email TEXT NOT NULL,
                                   mobile TEXT
                               );"""
    db_access.create_table(db_access.Connection(), sql_create_actor_table)


@pytest.fixture()
def create_actor(create_actor_table, client):
    form_data = dict(
        name="tester",
        email="tester@pwdmgr.com",
        mobile="9876543210",
        password="abc123$%^",
    )
    client.post("/signup", data=form_data)


@pytest.fixture()
def login_actor(create_actor, client):
    form_data = dict(
        name="tester",
        email="tester@pwdmgr.com",
        mobile="9876543210",
        password="abc123$%^",
    )
    client.post("/login", data=form_data)


@pytest.fixture()
def logout_actor(client):
    client.get("/logout")


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def create_profile_table(mock_db_file):
    sql_create_profile_table = """CREATE TABLE IF NOT EXISTS profile(
                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     actor_id INTEGER,
                                     app_name TEXT,
                                     user_id TEXT NOT NULL,
                                     user_name TEXT,
                                     password TEXT NOT NULL,
                                     password_expiry DATE,
                                     crn TEXT,
                                     profile_password TEXT,
                                     url TEXT,
                                     is_active BOOLEAN NOT NULL,
                                     customer_care_number TEXT,
                                     remarks VARCHAR(255),
                                     password_iv TEXT NOT NULL,
                                     profile_password_iv TEXT,
                                     FOREIGN KEY(actor_id) REFERENCES actor(id)
                               );"""
    db_access.create_table(db_access.Connection(), sql_create_profile_table)
