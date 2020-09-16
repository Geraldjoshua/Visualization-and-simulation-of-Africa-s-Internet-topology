import db
import time
import pandas as pd

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("/index.html", error=False)


@app.route('/simulate')
def simulate():
    # return render_template("/index.html", error=False)
    return render_template("/simulate.html", error=False)


# test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John", "age": 121})
    return "Connected to the data base!"
