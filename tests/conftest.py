from pathlib import Path

import pytest

from dao import db_access
from utils.constants import project_root


@pytest.fixture()
def create_actor_table(mocker):
    mocker.patch.object(db_access, "db_file", Path(f"{project_root}/test_password_manager.db"))

    sql_create_actor_table = """CREATE TABLE actor(
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   password TEXT NOT NULL,
                                   salt TEXT NOT NULL,
                                   name TEXT NOT NULL,
                                   email TEXT NOT NULL,
                                   mobile TEXT
                               );"""
    db_access.create_table(db_access.Connection(), sql_create_actor_table)
