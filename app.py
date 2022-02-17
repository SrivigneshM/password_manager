import os

from flask import Flask, render_template, request

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, "./")

app = Flask(__name__, template_folder=template_path)


@app.route("/", methods=["GET"])
def home():
    return render_template("templates/home.html")


@app.route("/password", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        password = request.form["field4"]
        return "Saved password: " + password


if __name__ == "__main__":
    app.run()
