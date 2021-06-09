from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(16), nullable=False)
    login_status = db.Column(db.Integer, nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))

class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    word_en = db.Column(db.String(32), nullable=False)
    word_type = db.Column(db.String(4), nullable=False)
    meanings = db.relationship('Meaning', backref='word', lazy=True)

class Meaning(db.Model):
    __tablename__ = 'meaning'
    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(200), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), nullable=False)
