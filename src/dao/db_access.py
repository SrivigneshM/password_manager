import sqlite3
from sqlite3 import Error

from utils.constants import Singleton, User, db_file


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


def get_user_by_id(conn, actor_id):
    """
    Query actor by id
    :param conn: the Connection object
    :param name: actor name
    :param password: actor password
    :return: user object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM actor WHERE id=?", (actor_id,))

    row = cur.fetchone()
    user = row if row else None

    user_obj = User("", "", user[3], user[4], user[5])
    return user_obj


def get_hashed_password(conn, name):
    """
    Query actor by name

    :param conn: the Connection object
    :param name: actor name
    :return: password
    """
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM actor WHERE name=?", (name,))

    row = cur.fetchone()
    password = row[1] if row else ""
    return password


def validate_profile(conn, actor_id, app_name):
    """
    Query profile by app_name and actor_id
    :param conn: the Connection object
    :param actor_id: actor id
    :param app_name: app name
    :return: id
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM profile WHERE actor_id=? and app_name=?", (actor_id, app_name))

    row = cur.fetchone()
    id = row[0] if row else -1

    return id


def read_profile(conn, actor_id, app_name):
    """
    Query profile by app_name and actor_id
    :param conn: the Connection object
    :param actor_id: actor id
    :param app_name: app name
    :return: profile_dict
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile WHERE actor_id=? and app_name=?", (actor_id, app_name))

    row = cur.fetchone()
    profile = row if row else None

    profile_dict = {
        "id": profile[0],
        "actor_id": profile[1],
        "app_name": profile[2],
        "user_id": profile[3],
        "user_name": profile[4],
        "password": profile[5],
        "password_expiry": profile[6],
        "crn": profile[7],
        "profile_password": profile[8],
        "url": profile[9],
        "is_active": profile[10],
        "customer_care_number": profile[11],
        "remarks": profile[12],
    }
    return profile_dict


def update_profile(conn, profile):
    """
    Update an existing profile in the profile table
    :param conn:
    :param profile:
    """
    try:
        sql = """ UPDATE profile
                  SET user_id = ?,
                      user_name = ?,
                      password = ?,
                      password_expiry = ?,
                      crn = ?,
                      profile_password = ?,
                      url = ?,
                      is_active = ?,
                      customer_care_number = ?,
                      remarks = ?
                  WHERE app_name = ? and actor_id = ? """
        cur = conn.cursor()
        cur.execute(sql, profile)
        conn.commit()
    except Error as e:
        repr(e)
        return False
    return True


def read_apps_list(conn, actor_id):
    """
    Query profiles by actor_id
    :param conn: the Connection object
    :param actor_id: actor id
    :return: apps_list
    """
    cur = conn.cursor()
    cur.execute("SELECT app_name FROM profile WHERE actor_id=?", (actor_id,))

    rows = cur.fetchall()

    apps_list = [row[0] for row in rows]
    return apps_list
