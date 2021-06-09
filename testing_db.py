from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USERNAME


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# class TestTable(db.Model):
#     __tablename__ = 'test_table'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     # def __repr__(self):
#     #     return '<User %r>' % self.username

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

# why in this file its working?
db.create_all()



if __name__ == '__main__':
    app.run(debug=True)