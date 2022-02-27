from flask import Flask, render_template, request

from dao.db_access import (
    Connection,
    create_actor,
    create_profile,
    validate_actor,
)
from utils.constants import Actor, Messages, Profile, project_root

app = Flask(__name__, template_folder=project_root)


@app.route("/", methods=["GET"])
def home():
    return render_template("templates/home.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        password = request.form["password"]
        salt = "random"
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        actor = Actor(password, salt, name, email, mobile)
        actor_id = create_actor(Connection(), actor)
        message = f"{Messages.SIGNUP_SUCCESS}{name}!"
        if actor_id < 0:
            message = f"{Messages.SIGNUP_FAILED}{name}!"
        return message


@app.route("/add_profile", methods=["POST"])
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


if __name__ == "__main__":
    app.run()
