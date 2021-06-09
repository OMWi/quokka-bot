from req_commands import send_message
from db_handler import *
from models import User

def registrate(chat_id, user_id):    
    send_message(chat_id, "Введите username и password через пробел")    
    if len(find_user_by_data("None", user_id)) == 0:
        newUser = User(user_id, "casual", chat_id, 1, 0, "None", "None")
        insert_user(newUser)
    


def login(chat_id, user_id):
    if len(find_user_by_id(user_id)) == 0:
        send_message(chat_id, "Вы не зарегестрированы")
        return;
    send_message(chat_id, "Введите username password через пробел")
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
        send_message(chat_id, "У вас не выполнен вход в аккаунт")
    else:
        update_user_login_status(user_id, username, 0)
        send_message(chat_id, "Выполнен выход")

def send_test(chat_id):
    words = get_random_words(4)
    msg = "Here are our words:\n {}".format(words)
    send_message(chat_id, msg)
    