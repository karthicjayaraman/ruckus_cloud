#from flask import Flask
from flask import Flask, render_template, g, redirect
import os


app = Flask(__name__)

@app.before_request
def db_connect():
	print "Called"

@app.route("/")
def hello():
    return "Flask inside Docker!!"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5005)

