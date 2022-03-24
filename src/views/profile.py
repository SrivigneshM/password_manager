import json

from flask import Blueprint, Response, request
from flask_login import current_user, login_required

from dao.db_access import (
    Connection,
    create_profile,
    read_apps_list,
    read_profile,
    update_profile,
    validate_actor,
    validate_profile,
)
from utils.constants import (
    STATUS_BAD_REQUEST,
    STATUS_OK,
    EditableProfile,
    Fields,
    Messages,
    Profile,
)

api_blueprint = Blueprint("profile_api", __name__)


@api_blueprint.route("/add_profile", methods=["POST", "PUT"])
@login_required
def add_profile():
    response_code = STATUS_OK
    app_name = request.form.get(Fields.APP_NAME, None)
    user_id = request.form.get(Fields.USER_ID, None)
    user_name = request.form.get(Fields.USER_NAME, None)
    password = request.form.get(Fields.PASSWORD, None)
    password_expiry = request.form.get(Fields.PASSWORD_EXPIRY, None)
    crn = request.form.get(Fields.CRN, None)
    profile_password = request.form.get(Fields.PROFILE_PASSWORD, None)
    url = request.form.get(Fields.URL, None)
    is_active = request.form.get(Fields.IS_ACTIVE, None)
    customer_care_number = request.form.get(Fields.CUSTOMER_CARE_NUMBER, None)
    remarks = request.form.get(Fields.REMARKS, None)

    actor_id = validate_actor(Connection(), current_user.name)
    if request.method == "POST" and validate_profile(Connection(), actor_id, app_name) > 0:
        message = f"{Messages.ADD_PROFILE_NAME_TAKEN}{app_name}!"
        response_code = STATUS_BAD_REQUEST
    elif request.method == "PUT":
        profile = EditableProfile(
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
            app_name,
            actor_id,
        )
        message = f"{Messages.EDIT_PROFILE_SUCCESS}{app_name}!"
        if not update_profile(Connection(), profile):
            message = f"{Messages.EDIT_PROFILE_FAILED}{app_name}!"
            response_code = STATUS_BAD_REQUEST
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
            response_code = STATUS_BAD_REQUEST
    return message, response_code


@api_blueprint.route("/read_profile", methods=["POST"])
@login_required
def get_profile():
    app_name = request.form.get(Fields.APP_NAME, None)
    actor_id = validate_actor(Connection(), current_user.name)
    payload = read_profile(Connection(), actor_id, app_name)
    resp = Response(json.dumps(payload), status=STATUS_OK, mimetype="application/json")
    return resp


@api_blueprint.route("/get_apps_list", methods=["POST"])
@login_required
def get_apps_list():
    actor_id = validate_actor(Connection(), current_user.name)
    payload = {"apps_list": read_apps_list(Connection(), actor_id)}
    resp = Response(json.dumps(payload), status=STATUS_OK, mimetype="application/json")
    return resp
