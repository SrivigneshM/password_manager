from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/print_password/<value>')
def print(value):
   return 'Entered password %s' % value 
  
@app.route('/password',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      password = request.form['password']
      return redirect(url_for('print',value = password))

if __name__ == "__main__":
  app.run()
