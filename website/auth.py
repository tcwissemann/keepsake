from flask import Blueprint, render_template, redirect, request, flash, redirect, url_for, render_template_string
from flask_mailman import EmailMessage
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        
        user_select = User.query.filter_by(email=email).first()
        if user_select:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(nickname) < 2:
            flash('Nickname must be more than 1 character.', category='error')
        elif password != password_check:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.dash'))
            
    return render_template("auth/sign_up.html", user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    #Not for people who are logged in.
    if current_user.is_authenticated:
        return redirect(url_for("views.dash"))
    
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_select = User.query.filter_by(email=user_email).first()
        
        if user_select:
            send_reset_password_email(user_select)
            
        #Ad ui for info in blue
        flash (
            "Instructions to reset your password were sent to your email address,"
            " if it exists in our system."
        )

        return redirect(url_for("auth.login"))

    return render_template ("auth/reset_password.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')    
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully!', category='success') 
                if remember:
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)
                    
                return redirect(url_for('views.dash'))
            else:
                flash('Invalid credentials, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        
    return render_template("auth/login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def send_reset_password_email(email):
    pass