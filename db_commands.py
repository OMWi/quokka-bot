from models import db, User, Account, Word, Meaning


# users

def insert_user(user:User):
    db.session.add(user)
    db.session.commit()


# accounts

def insert_account(account:Account):
    db.session.add(account)
    db.session.commit()


# words

def insert_word(word:Word):
    db.session.add(word)
    db.session.commit()


# meanings

def insert_meaning(meaning:Meaning):
    db.session.add(meaning)
    db.session.commit()