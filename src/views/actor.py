from flask import Blueprint, render_template, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from dao.db_access import (
    Connection,
    create_actor,
    get_hashed_password,
    get_user_by_id,
    validate_actor,
)
from utils.constants import STATUS_BAD_REQUEST, STATUS_OK, Actor, Fields, Messages

api_blueprint = Blueprint("actor_api", __name__)


@api_blueprint.route("/signup")
def signup():
    return render_template("signup.html")


@api_blueprint.route("/signup", methods=["POST"])
def signup_post():
    response_code = STATUS_OK
    password = request.form.get(Fields.PASSWORD, None)
    hashed = generate_password_hash(password, method="sha256")
    salt = "random"
    name = request.form.get(Fields.NAME, None)
    email = request.form.get(Fields.EMAIL, None)
    mobile = request.form.get(Fields.MOBILE, None)
    actor_id = validate_actor(Connection(), name)
    if actor_id > 0:
        message = f"{Messages.SIGNUP_NAME_TAKEN}{name}!"
        response_code = STATUS_BAD_REQUEST
    else:
        actor = Actor(hashed, salt, name, email, mobile)
        actor_id = create_actor(Connection(), actor)
        if actor_id > 0:
            message = f"{Messages.SIGNUP_SUCCESS}{name}!"
        else:
            message = f"{Messages.SIGNUP_FAILED}{name}!"
            response_code = STATUS_BAD_REQUEST
    return message, response_code


@api_blueprint.route("/login")
def login():
    return render_template("login.html")


@api_blueprint.route("/login", methods=["POST"])
def login_post():
    response_code = STATUS_OK
    password = request.form.get(Fields.PASSWORD, None)
    name = request.form.get(Fields.NAME, None)
    remember = True if request.form.get(Fields.REMEMBER) else False
    actor_id = validate_actor(Connection(), name)
    hashed_password = get_hashed_password(Connection(), name)
    if actor_id < 0 or not check_password_hash(hashed_password, password):
        message = f"{Messages.LOGIN_FAILED}!"
        response_code = STATUS_BAD_REQUEST
    else:
        user = get_user_by_id(Connection(), actor_id)
        if user:
            user.id = actor_id
            login_user(user, remember=remember)
        message = f"{Messages.LOGIN_SUCCESS}{name}!"
    return message, response_code


@api_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")
