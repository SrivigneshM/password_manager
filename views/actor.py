from flask import Blueprint, request

from dao.db_access import Connection, create_actor, validate_actor
from utils.constants import Actor, Messages

api_blueprint = Blueprint("actor_api", __name__)


@api_blueprint.route("/signup", methods=["POST"])
def signup():
    response_code = 200
    password = request.form.get("password", None)
    salt = "random"
    name = request.form.get("name", None)
    email = request.form.get("email", None)
    mobile = request.form.get("mobile", None)
    actor_id = validate_actor(Connection(), name)
    if actor_id > 0:
        message = f"{Messages.SIGNUP_NAME_TAKEN}{name}!"
        response_code = 400
    else:
        actor = Actor(password, salt, name, email, mobile)
        actor_id = create_actor(Connection(), actor)
        if actor_id > 0:
            message = f"{Messages.SIGNUP_SUCCESS}{name}!"
        else:
            message = f"{Messages.SIGNUP_FAILED}{name}!"
            response_code = 400
    return message, response_code
