from models import db, User, Account, Word, Meaning
from  sqlalchemy.sql.expression import func, select


def registrate_1(bot, chat_id, user_id):    
    user = User.query.filter_by(user_id = user_id).first()   
    if user is None:
        bot.send_message(chat_id=chat_id, text="Введите почту") 
        new_user = User(user_id, "user", 2)
        db.session.add(new_user)
        db.session.commit()
    else:
        if user.user_status == 1:
            bot.send_message(chat_id=chat_id, text="Для регистрации нового аккаунта сначала выйдите из текущего")
        elif user.user_status == 0:
            bot.send_message(chat_id=chat_id, text="Введите почту")
            user.user_status = 2
            db.session.commit()

def registrate_2(bot, chat_id, user_id, text):
    mail = text
    user = User.query.filter_by(user_id=user_id).first()
    mail_exists = db.session.query(Account.id).filter_by(mail=mail).first() is not None
    if mail_exists:
        bot.send_message(chat_id=chat_id, text="Почта {} уже занята".format(text.split()[0]))
        user.user_status = 0
        db.session.commit()
    else:
        new_account = Account(None, None, text.split()[0], 1)
        new_account.users.append(user)
        db.session.add(new_account)
        user.user_status = 3
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Как к вам обращаться?")

def registrate_3(bot, chat_id, user_id, text):
    name = text
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter(Account.users.any(user_id=user_id)).filter_by(account_status=1).first()
    account.username = name
    user.user_status = 4
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="{}, введите пароль".format(account.username))

def registrate_4(bot, chat_id, user_id, text):
    password = text.split()[0]
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter(Account.users.any(user_id=user_id)).filter_by(account_status=1).first()
    account.password = password
    user.user_status = 1
    account.account_status = 1
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Поздравляем с успешной регистрацией, {}".format(account.username))
    


def login_1(bot, chat_id, user_id):
    user = User.query.filter_by(user_id = user_id).first()
    if user is None:
        bot.send_message(chat_id=chat_id, text="Вы не зарегистрированы")
    elif user.user_status == 1:
        bot.send_message(chat_id=chat_id, text="Сначала выйдите из текущего аккаунта")
    else:
        user.user_status = 11
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Введите почту")

def login_2(bot, chat_id, user_id, text):
    user = User.query.filter_by(user_id = user_id).first()
    mail = text.split()[0]
    account = Account.query.filter_by(mail=mail).first()

    if account is None:
        bot.send_message(chat_id=chat_id, text="Аккаунт с почтой {} не найден".format(mail))
        user.user_status = 0
        db.session.commit()
    else:
        if account.account_status == 1:
            user.user_status = 0
            db.session.commit()
            bot.send_message(chat_id=chat_id, text=\
                "На аккаунта с почтой {} уже выполнен вход с другой учетной записи".format(mail))
        else:
            user.user_status = 12
            account.users.append(user)
            account.account_status = 2
            db.session.commit()
            bot.send_message(chat_id=chat_id, text="Введите пароль")
    
def login_3(bot, chat_id, user_id, text):
    password = text.split()[0]
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter(Account.users.any(user_id=user_id)).filter_by(account_status=2).first()
    # simultaneuos login?
    if password == account.password:
        user.user_status = 1
        account.account_status = 1
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Успешный вход. Добро пожаловать, {}".format(account.username))
    else:
        bot.send_message(chat_id=chat_id, text="Неверный пароль")

    

def logout(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None or user.user_status == 0:
        bot.send_message(chat_id=chat_id, text="У вас не выполнен вход в аккаунт")
    elif user.user_status == 1:
        account = Account.query.filter(Account.users.any(user_id=user_id)).filter_by(account_status=1).first()
        account.account_status = 0
        user.user_status = 0
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Произведен выход из аккаунта")


def word(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None or user.user_status == 0:
        bot.send_message(chat_id=chat_id, text="Функция не доступна")
    else:
        word = Word.query.order_by(func.rand()).first()
        str = "{} ({})\n".format(word.word_en, word.word_type)
        meanings = Meaning.query.filter_by(word_id=word.id).all()
        i = 1
        for elem in meanings:
            str += "{}. {}\n".format(i, elem.meaning)
            i += 1
        bot.send_message(chat_id=chat_id, text=str)