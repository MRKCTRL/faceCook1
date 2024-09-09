from . import db 
from flask_login import UserMixin
from datetime import datetime 


class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150), unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)
    diary_entries=db.relationship('DiaryEntry', backref='author', lazy=True)
    
class DiaryEntry(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(150), nullable=False)
    content=db.Column(db.text, nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    