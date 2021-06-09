from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(16), nullable=False)
    user_status = db.Column(db.Integer, nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

    def __init__(self, user_id, role, user_status):
        self.user_id = user_id
        self.role = role
        self.user_status = user_status

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    username = db.Column(db.String(32), nullable=True)
    password = db.Column(db.String(32), nullable=True)
    account_status = db.Column(db.Integer)

    def __init__(self, user_id, username, password, account_status):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.account_status  

class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    word_en = db.Column(db.String(32), nullable=False)
    word_type = db.Column(db.String(4), nullable=False)
    meanings = db.relationship('Meaning', backref='word', lazy=True)

    def __init__(self, word_en, word_type):
        self.word_en = word_en
        self.word_type = word_type

class Meaning(db.Model):
    __tablename__ = 'meaning'
    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(200), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), nullable=False)

    def __init__(self, meaning, word_id):
        self.meaning = meaning
        self.word_id = word_id

