from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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


class Login_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
