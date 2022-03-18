from flask import Blueprint, request

from dao.db_access import Connection, create_actor, validate_actor
from utils.constants import STATUS_BAD_REQUEST, STATUS_OK, Actor, Fields, Messages

api_blueprint = Blueprint("actor_api", __name__)


@api_blueprint.route("/signup", methods=["POST"])
def signup():
    response_code = STATUS_OK
    password = request.form.get(Fields.PASSWORD, None)
    salt = "random"
    name = request.form.get(Fields.NAME, None)
    email = request.form.get(Fields.EMAIL, None)
    mobile = request.form.get(Fields.MOBILE, None)
    actor_id = validate_actor(Connection(), name)
    if actor_id > 0:
        message = f"{Messages.SIGNUP_NAME_TAKEN}{name}!"
        response_code = STATUS_BAD_REQUEST
    else:
        actor = Actor(password, salt, name, email, mobile)
        actor_id = create_actor(Connection(), actor)
        if actor_id > 0:
            message = f"{Messages.SIGNUP_SUCCESS}{name}!"
        else:
            message = f"{Messages.SIGNUP_FAILED}{name}!"
            response_code = STATUS_BAD_REQUEST
    return message, response_code


@api_blueprint.route("/login")
def login():
    return "Login"


@api_blueprint.route("/logout")
def logout():
    return "Logout"
