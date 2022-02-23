from flask import Flask, render_template, request

from dao.db_access import Connection, create_actor
from utils.constants import Actor, Messages, project_root

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


if __name__ == "__main__":
    app.run()