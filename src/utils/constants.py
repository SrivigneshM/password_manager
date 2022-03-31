from collections import namedtuple
from pathlib import Path

from flask_login import UserMixin

project_root = Path(__file__).parent.parent.parent

db_file = Path(f"{project_root}/password_manager.db")


class Fields:
    REMEMBER = "remember"
    PASSWORD = "password"
    SALT = "salt"
    NAME = "name"
    EMAIL = "email"
    MOBILE = "mobile"
    ACTOR_ID = "actor_id"
    APP_NAME = "app_name"
    USER_ID = "user_id"
    USER_NAME = "user_name"
    PASSWORD_EXPIRY = "password_expiry"
    CRN = "crn"
    PROFILE_PASSWORD = "profile_password"
    URL = "url"
    IS_ACTIVE = "is_active"
    CUSTOMER_CARE_NUMBER = "customer_care_number"
    REMARKS = "remarks"
    ACTOR_NAME = "actor_name"
    ACTOR_PASSWORD = "actor_password"
    PASSWORD_IV = "password_iv"
    PROFILE_PASSWORD_IV = "profile_password_iv"


STATUS_OK = 200
STATUS_BAD_REQUEST = 400

Actor = namedtuple(
    "Actor", [Fields.PASSWORD, Fields.SALT, Fields.NAME, Fields.EMAIL, Fields.MOBILE]
)


class User(UserMixin, Actor):
    pass


Profile = namedtuple(
    "Profile",
    [
        Fields.ACTOR_ID,
        Fields.APP_NAME,
        Fields.USER_ID,
        Fields.USER_NAME,
        Fields.PASSWORD,
        Fields.PASSWORD_EXPIRY,
        Fields.CRN,
        Fields.PROFILE_PASSWORD,
        Fields.URL,
        Fields.IS_ACTIVE,
        Fields.CUSTOMER_CARE_NUMBER,
        Fields.REMARKS,
        Fields.PASSWORD_IV,
        Fields.PROFILE_PASSWORD_IV,
    ],
)
EditableProfile = namedtuple(
    "EditableProfile",
    [
        Fields.USER_ID,
        Fields.USER_NAME,
        Fields.PASSWORD,
        Fields.PASSWORD_EXPIRY,
        Fields.CRN,
        Fields.PROFILE_PASSWORD,
        Fields.URL,
        Fields.IS_ACTIVE,
        Fields.CUSTOMER_CARE_NUMBER,
        Fields.REMARKS,
        Fields.APP_NAME,
        Fields.ACTOR_ID,
    ],
)


class Singleton(type):
    """
    Metaclass approach to create singleton object in Python.
    Source:https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Messages:
    SIGNUP_SUCCESS = "Successfully signed up: "
    SIGNUP_FAILED = "Unable to signup: "
    SIGNUP_NAME_TAKEN = "Name is already taken: "
    LOGIN_SUCCESS = "Welcome: "
    LOGIN_FAILED = "Please check your login details and try again"
    ADD_PROFILE_SUCCESS = "Successfully added details for: "
    ADD_PROFILE_FAILED = "Unable to add details for: "
    ACTOR_VALIDATION_FAILED = "User name or password incorrect/ mismatched"
    ADD_PROFILE_NAME_TAKEN = "Application name is already present: "
    EDIT_PROFILE_SUCCESS = "Successfully updated details for: "
    EDIT_PROFILE_FAILED = "Unable to update details for: "
