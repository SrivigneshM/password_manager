from flask import Blueprint, request

from dao.db_access import Connection, create_profile, validate_actor
from utils.constants import Messages, Profile

api_blueprint = Blueprint("profile_api", __name__)


@api_blueprint.route("/add_profile", methods=["POST"])
def add_profile():
    actor_name = request.form["actor_name"]
    actor_password = request.form["actor_password"]
    app_name = request.form["app_name"]
    user_id = request.form["user_id"]
    user_name = request.form["user_name"]
    password = request.form["password"]
    password_expiry = request.form["password_expiry"]
    crn = request.form["crn"]
    profile_password = request.form["profile_password"]
    url = request.form["url"]
    is_active = request.form["is_active"]
    customer_care_number = request.form["customer_care_number"]
    remarks = request.form["remarks"]

    actor_id = validate_actor(actor_name, actor_password)
    if actor_id < 0:
        message = f"{Messages.ACTOR_VALIDATION_FAILED}!"
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
    return message
