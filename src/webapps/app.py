import secrets
from datetime import timedelta
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
# Below flag to be tested after setting domain name for the app
# app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=2)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
# Below flag to be enbled after making the app HTTPS
# app.config["SESSION_COOKIE_SECURE"] = True
app.config["SERVER_NAME"] = "localhost:5000"
app.register_blueprint(actor_api_blueprint)
app.register_blueprint(profile_api_blueprint)

login_manager = LoginManager()
login_manager.login_view = "actor_api.login"
login_manager.init_app(app)
login_manager.session_protection = "strong"


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


if __name__ == "__main__":
    # context = (f"{project_root}/ssl/simvault.crt", f"{project_root}/ssl/simvault.key")
    app.run()
