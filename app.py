from flask import Flask, redirect, url_for, request, render_template

import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)


@app.route('/', methods = ['GET'])
def home():
   return render_template('templates/home.html')


@app.route('/password',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      password = request.form['field4']
      return "Saved password: " + password


if __name__ == "__main__":
  app.run()
