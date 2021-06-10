from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


account_user = db.Table('account_user',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
)

#many-to-many
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(16), nullable=False)
    user_status = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, role, user_status):
        self.user_id = user_id
        self.role = role
        self.user_status = user_status

    def __str__(self) -> str:
        return f"user_id: {self.user_id}, role: {self.role}, status: {self.user_status}"

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=True)
    password = db.Column(db.String(32), nullable=True)
    mail = db.Column(db.String(32), nullable=False, unique=True)
    account_status = db.Column(db.Integer)
    users = db.relationship('User', secondary=account_user,\
        backref=db.backref('accounts'))

    def __init__(self, username, password, mail, account_status):
        self.username = username
        self.password = password
        self.account_status = account_status
        self.mail = mail

    def __str__(self):
        return f"account_id: {self.id}, name: {self.username}, mail: {self.password}, status: {self.account_status}"


#one-to-many
class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    word_en = db.Column(db.String(32), nullable=False)
    word_type = db.Column(db.String(4), nullable=False)
    meanings = db.relationship('Meaning', backref='word', lazy=True)

    def __init__(self, word_en, word_type):
        self.word_en = word_en
        self.word_type = word_type
    
    def __str__(self):
        return f"word_id: {self.id}, word_en: {self.word_en}, word_type: {self.word_type}"

class Meaning(db.Model):
    __tablename__ = 'meaning'
    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(200), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), nullable=False)

    def __init__(self, meaning, word_id):
        self.meaning = meaning
        self.word_id = word_id

    def __str__(self):
        return f"meaning_id: {self.id}, word_id: {self.word_id}, meaning: {self.meaning}"

