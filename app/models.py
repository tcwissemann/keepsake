from . import db, app
from flask_login import UserMixin
from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='basic')
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    Nations = db.relationship('Nation')

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

class Nation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(150), unique=True, nullable=False)
    nation_name = db.Column(db.String(150), unique=True, nullable=False)
    nation_password = db.Column(db.String(150), nullable=False)
    service_type = db.Column(db.String(150), nullable=False)
    mode = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(150), nullable=False, default='incomplete')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ServiceMode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    service = db.Column(db.String(150), unique=False, nullable=True)
