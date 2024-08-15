from flask import Blueprint, render_template, redirect, request, flash, redirect, url_for, render_template_string
from flask_mailman import EmailMessage
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from website.forms import SignUpForm, LoginForm, ForgotPasswordForm

#contains routes and endpoints pertaining to authentication
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('An account with this email already exists!', category='error')
            else:
                db.session.add(User(email=form.email.data, nickname=form.username.data, password=generate_password_hash(form.password.data, method='scrypt')))
                db.session.commit()
                return redirect(url_for('auth.login'))
    return render_template("auth/sign_up.html", form=form, user=current_user)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_password.data)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.dash'))
            flash('Invalid credentials or email does not exist.', category='error')
    return render_template("auth/login.html", form=form, user=current_user)


@auth.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Please check your email for instructions.')
            return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def send_reset_password_email(email):
    pass












# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         nickname = request.form.get('nickname')
#         password = request.form.get('password')
#         password_check = request.form.get('password_check')

#         user_select = User.query.filter_by(email=email).first()
#         if user_select:
#             flash('Email already exists!', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 4 characters.', category='error')
#         elif len(nickname) < 2:
#             flash('Nickname must be more than 1 character.', category='error')
#         elif password != password_check:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password) < 7:
#             flash('Password must be greater than 7 characters.', category='error')
#         else:
#             new_user = User(email=email, nickname=nickname, password=generate_password_hash(password, method='scrypt'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('views.dash'))

#     return render_template("auth/sign_up.html", user=current_user)

# @auth.route('/reset-password', methods=['GET', 'POST'])
# def reset_password():
#     #Not for people who are logged in.
#     if current_user.is_authenticated:
#         return redirect(url_for("views.dash"))

#     if request.method == 'POST':
#         user_email = request.form.get('email')
#         user_select = User.query.filter_by(email=user_email).first()

#         if user_select:
#             send_reset_password_email(user_select)

#         #Ad ui for info in blue
#         flash (
#             "Instructions to reset your password were sent to your email address,"
#             " if it exists in our system."
#         )

#         return redirect(url_for("auth.login"))

#     return render_template ("auth/reset_password.html", user=current_user)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = request.form.get('remember')

#         user = User.query.filter_by(email=email).first()

#         if user:
#             if check_password_hash(user.password, password):
#                 flash('Logged in succesfully!', category='success')
#                 if remember:
#                     login_user(user, remember=True)
#                 else:
#                     login_user(user, remember=False)

#                 return redirect(url_for('views.dash'))
#             else:
#                 flash('Invalid credentials, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

#     return render_template("auth/login.html", user=current_user)

