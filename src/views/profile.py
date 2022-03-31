import ast
import json

from Crypto.Random import get_random_bytes
from flask import Blueprint, Response, request
from flask_login import current_user, login_required

from dao.db_access import (
    Connection,
    create_profile,
    read_apps_list,
    read_profile,
    update_profile,
    update_profile_password_iv,
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
from utils.crypto import get_instance

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
    is_active = request.form.get(Fields.IS_ACTIVE, "off")
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
        message, response_code = update(profile, app_name)
    else:
        password_iv = get_random_bytes(16)
        profile_password_iv = get_random_bytes(16) if profile_password else None
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
            password_iv,
            profile_password_iv,
        )
        message, response_code = add(profile, app_name)
    return message, response_code


def add(profile, app_name):
    message = f"{Messages.ADD_PROFILE_FAILED}{app_name}!"
    response_code = STATUS_BAD_REQUEST
    iv = profile.password_iv
    if profile.password:
        profile = profile._replace(
            password=encrypt_password(profile.actor_id, profile.password, iv), password_iv=str(iv)
        )
        if profile.profile_password:
            iv = profile.profile_password_iv
            profile = profile._replace(
                profile_password=encrypt_password(profile.actor_id, profile.profile_password, iv),
                profile_password_iv=str(iv),
            )
        profile_id = create_profile(Connection(), profile)
        if profile_id > 0:
            message = f"{Messages.ADD_PROFILE_SUCCESS}{app_name}!"
            response_code = STATUS_OK
    return message, response_code


def update(profile, app_name):
    message = f"{Messages.EDIT_PROFILE_FAILED}{app_name}!"
    response_code = STATUS_BAD_REQUEST
    actor_id = profile.actor_id

    if profile.password:
        db_profile = read_profile(Connection(), actor_id, app_name)
        db_pwd_iv = db_profile.get("password_iv")
        iv = ast.literal_eval(db_pwd_iv)
        profile = profile._replace(
            password=encrypt_password(profile.actor_id, profile.password, iv)
        )
        if update_profile(Connection(), profile):
            db_pwd_iv = db_profile.get("profile_password_iv", None)
            iv = ast.literal_eval(db_pwd_iv) if db_pwd_iv is not None else get_random_bytes(16)
            if profile.profile_password:
                profile_password = encrypt_password(actor_id, profile.profile_password, iv)
                profile_password_iv = str(iv)
                update_profile_password_iv(
                    Connection(), profile_password, profile_password_iv, actor_id, app_name
                )
            message = f"{Messages.EDIT_PROFILE_SUCCESS}{app_name}!"
            response_code = STATUS_OK

    return message, response_code


def encrypt_password(actor_id, password, iv):
    aes_cipher = get_instance(actor_id)
    enc = aes_cipher.encrypt(password, iv)
    return str(enc)


def decrypt_password(actor_id, enc, iv):
    aes_cipher = get_instance(actor_id)
    enc = ast.literal_eval(enc)
    iv = ast.literal_eval(iv)
    dec = aes_cipher.decrypt(enc, iv)
    return dec


@api_blueprint.route("/read_profile", methods=["POST"])
@login_required
def get_profile():
    app_name = request.form.get(Fields.APP_NAME, None)
    actor_id = validate_actor(Connection(), current_user.name)
    payload = read_profile(Connection(), actor_id, app_name)
    payload["password"] = decrypt_password(
        actor_id, payload.get("password"), payload.get("password_iv")
    )
    if payload.get("profile_password", None):
        payload["profile_password"] = decrypt_password(
            actor_id, payload.get("profile_password"), payload.get("profile_password_iv")
        )
    resp = Response(json.dumps(payload), status=STATUS_OK, mimetype="application/json")
    return resp


@api_blueprint.route("/get_apps_list")
@login_required
def get_apps_list():
    actor_id = validate_actor(Connection(), current_user.name)
    payload = {"apps_list": read_apps_list(Connection(), actor_id)}
    resp = Response(json.dumps(payload), status=STATUS_OK, mimetype="application/json")
    return resp
