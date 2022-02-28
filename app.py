from flask import Flask, render_template

from utils.constants import project_root
from views.actor import api_blueprint as actor_api_blueprint
from views.profile import api_blueprint as profile_api_blueprint

app = Flask(__name__, template_folder=project_root)

app.register_blueprint(actor_api_blueprint)
app.register_blueprint(profile_api_blueprint)


@app.route("/", methods=["GET"])
def home():
    return render_template("templates/home.html")


if __name__ == "__main__":
    app.run()
