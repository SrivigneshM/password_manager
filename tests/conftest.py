from pathlib import Path

import pytest

from dao import db_access
from utils.constants import Actor, project_root


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
def create_actor(create_actor_table):
    actor = Actor("abc123$%^", "random", "tester", "tester@pwdmgr.com", "1234567890")
    db_access.create_actor(db_access.Connection(), actor)


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
                                     FOREIGN KEY(actor_id) REFERENCES actor(id)
                               );"""
    db_access.create_table(db_access.Connection(), sql_create_profile_table)
