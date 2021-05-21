from enum import unique
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from forms import Registration_form, Login_form


# configure app, db
app = Flask(__name__)
app.config["SECRET_KEY"] = "720e9e855f1fd7b6f91668af1c4f5f37"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plans.db"
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# configure session (TODO)??


# task table
class task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False, default="ToDo")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    parentid = db.Column(db.Integer)

    def __repr__(self):
        return f"Task('{self.id}', '{self.type}', {self.content}')"


# user table
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    hash = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code


# index page
@app.route("/")
def index():
    return render_template("index.html")


# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration_form()
    return render_template("register.html", title="Register", form=form)


#     if request.method == "GET":
#         return render_template("register.html")

#     else:
#         username = request.form.get("username")
#         email = request.form.get("email")
#         password = request.form.get("password")
#         confirmation = request.form.get("password")

#         hash = generate_password_hash(password)

#         new_user = user(username=username, email=email, hash=hash)

#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             return redirect("/")
#         except:
#             return apology("Something went wrong, user is not registered ;(", 500)

#         # check

#         return "apology"


@app.route("/login")
def login():
    form = Login_form()
    return render_template("login.html", title="Login", form=form)
    #
    return "apology"


@app.route("/logout")
def logout():
    return "apology"


@app.route("/new")
def new():
    return ""


@app.route("/update")
def update():
    return ""


@app.route("/lookup")
def lookup():
    pass


@app.route("/settings")
def settings():
    pass


@app.route("/apology")
def apology():
    pass


if __name__ == "__main__":
    app.run(debug=True)
