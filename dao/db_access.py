import sqlite3
from sqlite3 import Error

from utils.constants import Singleton, db_file


def create_connection():
    """create a database connection to the SQLite database
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        repr(e)

    return conn


class Connection(metaclass=Singleton):
    def __new__(cls):
        return create_connection()


def create_actor(conn, actor):
    """
    Create a new actor into the actor table
    :param conn:
    :param actor:
    :return: actor_id
    """
    actor_id = -1
    try:
        sql = """ INSERT INTO actor(password, salt, name, email, mobile)
                  VALUES(?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, actor)
        conn.commit()
        actor_id = cur.lastrowid
    except Error as e:
        repr(e)

    return actor_id
