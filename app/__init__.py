import os
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy()
mail = Mail(app)

def create_app():
    #Ensure the database directory exists
    database_path = app.config['DATABASE_PATH']
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    db.init_app(app)

    #create models
    from .models import User, Keep
    with app.app_context():
        db.create_all()

    #Import/Register Blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #login manager
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

