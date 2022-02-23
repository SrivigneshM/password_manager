from collections import namedtuple
from pathlib import Path

project_root = Path(__file__).parent.parent

db_file = Path(f"{project_root}/password_manager.db")

Actor = namedtuple("Actor", ["password", "salt", "name", "email", "mobile"])


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