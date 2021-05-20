from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plans.db"
db = SQLAlchemy(app)


class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False, default="ToDo")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    duration = db.Column(db.DateTime)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("register")
def register():
    return "apology"


@app.route("login")
def login():
    return "apology"


@app.route("new")
def new():
    return ""


@app.route("lookup")
def lookup():
    pass


@app.route("settings")
def settings():
    pass


@app.route("apology")
def apology():
    pass


if __name__ == "__main__":
    app.run(debug=True)
