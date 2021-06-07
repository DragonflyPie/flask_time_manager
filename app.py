from enum import unique
from re import A
from flask import Flask, redirect, render_template, request, flash, url_for, abort, jsonify
from flask.sessions import NullSession
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import date, datetime, timezone
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
#from forms import Registration_form, Login_form
from flask_login import LoginManager, login_manager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField, DecimalField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional
from sqlalchemy import func
from datetime import date



# configure app, db
app = Flask(__name__)
app.config["SECRET_KEY"] = "720e9e855f1fd7b6f91668af1c4f5f37"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plans.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' #class for flash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    hash = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# task table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False, default="task")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    monday = db.Column(db.Boolean)
    tuesday = db.Column(db.Boolean)
    wednesday = db.Column(db.Boolean)
    thursday = db.Column(db.Boolean)
    friday = db.Column(db.Boolean)
    saturday = db.Column(db.Boolean)
    sunday = db.Column(db.Boolean)

    def __repr__(self):
        return f"Task('{self.id}', '{self.user_id}', '{self.type}', {self.content}', {self.done})"

class Registration_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email('This e-mail adress is not valid')])
    password = PasswordField("Password", validators=[DataRequired(), ])
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


class Objective_form(FlaskForm):
    content = TextAreaField("Objective", validators=[DataRequired("Doing nothing is not a plan!")])
    type = RadioField("Type", id = "radioweek", choices=[('task', 'Task'), ('routine', 'Routine'), ('goal', 'Goal')], default = 'task')
    monday = BooleanField("Monday", default="checked")
    tuesday = BooleanField("Tuesday", default="checked")
    wednesday = BooleanField("Wednesday", default="checked")
    thursday = BooleanField("Thursday", default="checked")
    friday = BooleanField("Friday", default="checked")
    saturday = BooleanField("Saturday", default="checked")
    sunday = BooleanField("Sunday", default="checked")
    submit = SubmitField("Submit new objective")

def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

# index page
@app.route("/", methods=["GET", "POST"])
def index():
    today = date.today()
    return redirect (url_for("lookup", searchdate = today))
    if request.method == "POST":
        searchdate = request.form["datepicker"]
        return redirect(url_for("lookup", searchdate=searchdate))
    else:
        if not current_user.is_authenticated:
            return redirect(url_for("welcome"))
        today = date.today()
        tasks = Task.query.filter_by(user_id=current_user.id, parent_id = None)
        subtasks = Task.query.filter(Task.parent_id != None).filter_by(user_id=current_user.id)
                    
        return render_template("index.html", tasks=tasks, subtasks=subtasks)

@app.route("/lookup/<searchdate>", methods=["GET", "POST"])
@login_required
def lookup(searchdate):
    if request.method == "POST":
        searchdate = request.form["datepicker"]
        return redirect(url_for("lookup", searchdate=searchdate))
    else:
        date_dateformat = datetime.strptime(searchdate, "%Y-%m-%d").date()
        week_int = date_dateformat.weekday()
        def dayofweek(i):
            switcher={
                0:'monday',
                1:'tuesday',
                2:'wednesday',
                3:'thursday',
                4:'friday',
                5:'saturday',
                6:'sunday',
            }
            return switcher.get(i)
        day = (dayofweek(week_int))

        tasks = Task.query.filter(Task.user_id==current_user.id, Task.parent_id == None, Task.type == "task", Task.done == False).filter(func.date(Task.datetime) == date_dateformat)
        subtasks = Task.query.filter(Task.parent_id != None, Task.type == "task").filter_by(user_id=current_user.id)
        goals = Task.query.filter(Task.user_id==current_user.id, Task.type == "goal", Task.done == False).filter(func.date(Task.datetime) >= date_dateformat)
        routines = Task.query.filter(Task.user_id == current_user.id).filter(getattr(Task, day) == True)
        return render_template("lookup.html", tasks=tasks, subtasks=subtasks, routines=routines, goals=goals, date_dateformat=date_dateformat)




# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Login_form()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for("index"))
        else:
            flash('Nope. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/new", methods=["GET", "POST"])
@login_required
def new_object():
    form = Objective_form()
    if request.method == 'POST' and form.validate_on_submit():
        task = Task(content = form.content.data, type = form.type.data, user=current_user)
        if task.type != "routine":
            if request.form["datetime"] != "":
                timestamp = int(request.form["datetime"])
                objective_time = datetime.fromtimestamp(timestamp)
            else:
                objective_time = None
            task.datetime = objective_time
        else:
            task.monday = form.monday.data
            task.tuesday = form.tuesday.data
            task.wednesday = form.wednesday.data
            task.thursday = form.thursday.data
            task.friday = form.friday.data
            task.saturday = form.saturday.data
            task.sunday = form.sunday.data
        db.session.add(task)
        db.session.commit()
        flash('New objective is set', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('new.html', title = "New objective", form=form, legend="What are we going to do?", parent_objective = None)


@app.route("/add/<int:task_id>", methods=["GET", "POST"])
@login_required
def new_subobjective(task_id):
    form = Objective_form()
    parent_objective = Task.query.get_or_404(task_id)
    if request.method == 'POST' and form.validate_on_submit():
        task = Task(content = form.content.data, type = form.type.data, user=current_user, parent_id = task_id)
        if task.type != "routine":
            if request.form["datetime"] != "":
                timestamp = int(request.form["datetime"])
                objective_time = datetime.fromtimestamp(timestamp)
            else:
                objective_time = None
            task.datetime = objective_time
        else:
            task.monday = form.monday.data
            task.tuesday = form.tuesday.data
            task.wednesday = form.wednesday.data
            task.thursday = form.thursday.data
            task.friday = form.friday.data
            task.saturday = form.saturday.data
            task.sunday = form.sunday.data
        db.session.add(task)
        db.session.commit()
        flash('New subobjective is set', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('new.html', title = "New subobjective", form=form, legend="What are we going to do?", parent_objective = parent_objective)


@app.route("/done/<int:task_id>", methods =["POST"])
@login_required
def done(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    task.done = True
    db.session.commit()
    flash('Done', 'success')
    return redirect(url_for('index'))


@app.route("/update/<int:task_id>", methods=["GET", "POST"])
@login_required
def update(task_id):
    form = Objective_form()    
    task = Task.query.get_or_404(task_id)
    parent_task = Task.query.get(task.parent_id)
    
    if task.user != current_user:
        abort(403)
    if request.method == "POST" and form.validate_on_submit():
        task.content = form.content.data
        task.type = form.type.data  
        if task.type != "routine":
            if request.form["datetime"] != "":
                objective_time = datetime.strptime(request.form["datetime"], "%Y-%m-%d %H-%M")
            else:
                objective_time = None
            task.datetime = objective_time

        else:
            task.monday = form.monday.data
            task.tuesday = form.tuesday.data
            task.wednesday = form.wednesday.data
            task.thursday = form.thursday.data
            task.friday = form.friday.data
            task.saturday = form.saturday.data
            task.sunday = form.sunday.data
        db.session.commit()
        flash('Objective updated', 'success')
        return redirect(url_for('index'))
    else:
        form.content.data = task.content
        form.type.data = task.type
        return render_template('update.html', title = "Update", task=task, form=form, legend="Update task", parent_task=parent_task)


@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Objective deleted', 'success')
    return redirect(url_for('index'))


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="Account settings")


@app.route("/apology")
def apology():
    pass


if __name__ == "__main__":
    app.run(debug=True)
