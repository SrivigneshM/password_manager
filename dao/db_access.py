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


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        repr(e)


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


def create_profile(conn, profile):
    """
    Create a new profile into the profile table
    :param conn:
    :param profile:
    :return: profile_id
    """
    profile_id = -1
    try:
        sql = """ INSERT INTO profile(actor_id, app_name, user_id, user_name,
                  password, password_expiry, crn, profile_password, url,
                  is_active, customer_care_number, remarks)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, profile)
        conn.commit()
        profile_id = cur.lastrowid
    except Error as e:
        repr(e)

    return profile_id


def validate_actor(conn, name, password=None):
    """
    Query actor by name
    :param conn: the Connection object
    :param name: actor name
    :param password: actor password
    :return: id
    """
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM actor WHERE name=?", (name,))

    rows = cur.fetchall()

    for row in rows:
        if (password is None) or row[1] == password:
            return row[0]
    return -1
