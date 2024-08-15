from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime,timezone

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
    nickname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='basic')
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    keepsakes = db.relationship('Keep')
