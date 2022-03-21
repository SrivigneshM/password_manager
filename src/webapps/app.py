import secrets
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager

from utils.constants import User, project_root
from views.actor import api_blueprint as actor_api_blueprint
from views.profile import api_blueprint as profile_api_blueprint

app = Flask(
    __name__,
    template_folder=Path(f"{project_root}/templates"),
    static_folder=Path(f"{project_root}/static"),
)

app.config["SECRET_KEY"] = secrets.token_hex(16)
app.register_blueprint(actor_api_blueprint)
app.register_blueprint(profile_api_blueprint)

login_manager = LoginManager()
login_manager.login_view = "actor.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


@app.route("/edit_profile", methods=["GET"])
def edit_profile():
    return render_template("edit.html")


if __name__ == "__main__":
    app.run()
