from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
#Requires email_validator installed to work

class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    accept_tos = BooleanField(label='I\'ve read the terms and conditions', validators=[DataRequired()])
    submit = SubmitField(label='Sign Up', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    remember_password = BooleanField(label='Remember Password')
    submit = SubmitField(label='Login', validators=[DataRequired()])

class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Send Link', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Change Password', validators=[DataRequired()])

class NationForm(FlaskForm):
    nation_name = StringField(label='Nation Name', validators=[DataRequired(), Length(min=2, max=40)])
    nation_password = PasswordField(label='Nation Password', validators=[DataRequired(), Length(min=2, max=32)])
    service_type = SelectField(label='Service Type', choices=[('', 'Select Service'), ('issue_handler', 'Issue Handler'), ('score_maximizer', 'Score Maximizer'), ('score_minimizer', 'Score Minimizer'), ('scheduled_logins', 'Scheduled Logins')], validators=[DataRequired()])
    mode = SelectField(label='Mode', coerce=int, validators=[DataRequired()])
    submit = SubmitField(label='Add', validators=[DataRequired()])