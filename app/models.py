from . import db, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer

class Keep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#rename nickname to username accross app
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='basic')
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    keepsakes = db.relationship('Keep')

    #generates json token with 15 minute expiration
    def get_token(self, expires_sec=900):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id':self.id})

    @staticmethod
    def verify_token(token, expires_sec=900):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    #generates json token with 15 minute expiration
    def get_token(self, expires_sec=900):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id':self.id})

    @staticmethod
    def verify_token(token, expires_sec=900):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return Register.query.get(user_id)