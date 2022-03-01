from flask import Blueprint, request

from dao.db_access import Connection, create_profile, validate_actor
from utils.constants import Messages, Profile

api_blueprint = Blueprint("profile_api", __name__)


@api_blueprint.route("/add_profile", methods=["POST"])
def add_profile():
    response_code = 200
    actor_name = request.form.get("actor_name", None)
    actor_password = request.form.get("actor_password", None)
    app_name = request.form.get("app_name", None)
    user_id = request.form.get("user_id", None)
    user_name = request.form.get("user_name", None)
    password = request.form.get("password", None)
    password_expiry = request.form.get("password_expiry", None)
    crn = request.form.get("crn", None)
    profile_password = request.form.get("profile_password", None)
    url = request.form.get("url", None)
    is_active = request.form.get("is_active", None)
    customer_care_number = request.form.get("customer_care_number", None)
    remarks = request.form.get("remarks", None)

    actor_id = validate_actor(Connection(), actor_name, actor_password)
    if actor_id < 0:
        message = f"{Messages.ACTOR_VALIDATION_FAILED}!"
        response_code = 400
    else:
        profile = Profile(
            actor_id,
            app_name,
            user_id,
            user_name,
            password,
            password_expiry,
            crn,
            profile_password,
            url,
            is_active,
            customer_care_number,
            remarks,
        )
        profile_id = create_profile(Connection(), profile)
        message = f"{Messages.ADD_PROFILE_SUCCESS}{app_name}!"
        if profile_id < 0:
            message = f"{Messages.ADD_PROFILE_FAILED}{app_name}!"
            response_code = 400
    return message, response_code
