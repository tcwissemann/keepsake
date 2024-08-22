import os
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy()
DB_NAME = "app.db"
mail = Mail(app)

def create_app():
    #should be better than this
    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')

    #Ensure the database directory exists
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(database_path, DB_NAME)}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Keep

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', category='error')
        return redirect(url_for('auth.login'))

    return app

