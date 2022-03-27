import secrets
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from dao.db_access import Connection, get_user_by_id
from utils.constants import project_root
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
login_manager.login_view = "actor_api.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(Connection(), int(user_id))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@app.route("/edit_profile", methods=["GET"])
@login_required
def edit_profile():
    return render_template("edit.html")


if __name__ == "__main__":
    app.run()
