from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	content = db.Column(db.String(100), nullable=False)
	result = db.Column(db.String(100), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))