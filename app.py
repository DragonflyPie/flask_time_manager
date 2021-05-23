from enum import unique
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
#from forms import Registration_form, Login_form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


# configure app, db
app = Flask(__name__)
app.config["SECRET_KEY"] = "720e9e855f1fd7b6f91668af1c4f5f37"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plans.db"
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# configure session (TODO)??


# task table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False, default="ToDo")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.user_id}', '{self.type}', {self.content}')"


# user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    hash = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Registration_form(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmation = PasswordField(
        "Confirmation", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username already exists.")

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already in use by existing user.")


class Login_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


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
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, hash = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Registration successfull. Welcome aboad, {form.username.data}!", "success"
        )
        return redirect(url_for("login"))
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        if form.email.data == '123@mail.ru' and form.password.data == 'password':
            flash('Welcome back!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nope. Please check username and password', 'danger')
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
