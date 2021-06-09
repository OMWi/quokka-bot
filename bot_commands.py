from app import bot
from models import db, User, Account, Word, Meaning


def registrate(chat_id, user_id):    
    user = User.query.filter_by(user_id = user_id)     
    if user is None:
        bot.send_message(chat_id=chat_id, text="Введите логин и пароль через пробел") 
        newUser = User(user_id, "user", 2)
        db.session.add(newUser)
        db.session.commit()
    else:
        if user.login_status == 1:
            bot.send_message(chat_id=chat_id, text="Для регистрации нового аккаунта выйдите из текущего")


def login(chat_id, user_id):
    user = User.query.filter_by(user_id = user_id)
    
    if len(find_user_by_id(user_id)) == 0:
        bot.send_message(chat_id=chat_id, text="Вы не зарегестрированы")
        return;
    bot.send_message(chat_id=chat_id, text="Введите username password через пробел")
    update_user_status(user_id, 2)

def logout(chat_id, user_id):
    user_statuses = get_login_status(user_id)
    login_status = 0
    username = ""
    for elem in user_statuses:
        if elem[0] != 0:
            login_status = elem[0]
            username = elem[1]
            break
    if login_status == 0:
        bot.send_message(chat_id=chat_id, text="У вас не выполнен вход в аккаунт")
    else:
        update_user_login_status(user_id, username, 0)
        bot.send_message(chat_id=chat_id, text="Выполнен выход")

def send_test(chat_id):
    words = get_random_words(4)
    msg = "Here are our words:\n {}".format(words)
    bot.send_message(chat_id=chat_id, text=msg)
    