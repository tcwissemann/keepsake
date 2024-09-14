from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import User, Register
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import ResetPasswordForm, SignUpForm, LoginForm, ResetRequestForm
from flask_mail import Message

#contains routes and endpoints pertaining to authentication
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
            user_exists = User.query.filter_by(email=form.email.data).first()
            user_register_exists = Register.query.filter_by(email=form.email.data).first()
            if user_exists:
                flash('An account with this email already exists!', category='error')
            else:
                new_user = Register(email=form.email.data, username=form.username.data, password=generate_password_hash(form.password.data, method='scrypt'))
                if not user_register_exists:
                    db.session.add(new_user)
                    db.session.commit()
                send_registration_email(new_user)
                flash('Account created, please check your email to verify your account!')
                return redirect(url_for('auth.login'))
    return render_template("auth/sign_up.html", form=form, user=current_user)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.data)
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_password.data)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.dashboard'))
        flash('Invalid credentials or email does not exist.', category='error')
    return render_template("auth/login.html", form=form, user=current_user)

#registration email flow
def send_registration_email(user):
    token = user.get_token()
    msg = Message('Registration Email', recipients=[user.email], sender='ns.toolkit.helper@gmail.com')
    msg.body = f''' To create your account please follow the link below:

    {url_for('auth.register_token', token=token, _external=True)}

    If you didn't send a password reset request, please ignore this message.
    The link will expire in 15 minutes.
    '''
    mail.send(msg)
    # print(f"Failed to send email: {e}")
    # flash('Failed to send registration email. Please try again later.', category='error')

@auth.route('confirm-registration/<token>', methods=['POST', 'GET'])
def register_token(token):
    register_user = Register.verify_token(token=token)
    if register_user is None:
        flash('Sorry, this link has expired', category='error')
        return redirect(url_for('auth.sign_up'))
    else:
        user = User(email=register_user.email, username=register_user.username, password=register_user.password)
        db.session.add(user)
        db.session.commit()
        # Remove from Register after successful registration
        db.session.delete(register_user)
        db.session.commit()
        flash('Successfully created account, please log in!', category='success')
        return redirect(url_for('auth.login'))

    # return render_template('auth/change_password.html', form=form, user=current_user)

#Password Reset
@auth.route('/reset-password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = ResetRequestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_reset_request(user)
            flash('Please check your email for instructions.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid Submission', category='error')
    return render_template('auth/forgot_password.html', form=form, user=current_user)

def send_reset_request(user):
    token=user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='ns.toolkit.helper@gmail.com')
    msg.body = f''' To reset your password please follow the link below:

    {url_for('auth.reset_token', token=token, _external=True)}

    If you didn't send a password reset request, please ignore this message.
    The link will expire in 15 minutes.
    '''
    mail.send(msg)

@auth.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    user=User.verify_token(token=token)
    if user is None:
        flash('Sorry, this link has expired', category='error')
        return redirect(url_for('auth.reset_request'))

    form=ResetPasswordForm()
    if request.method == 'POST':
        print(form.password.data)
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='scrypt')
            print(hashed_password)
            user.password=hashed_password
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid Submisson', category='error')
    return render_template('auth/change_password.html', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#ADD Delete Account Option