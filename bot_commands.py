from req_commands import send_message
from db_handler import get_random_words, create_connection, find_user, get_status, set_login_status, set_status, get_login_status
from models import User
import config

def registrate(chat_id, user_id):
    if len(find_user(user_id)) > 0:
        send_message(chat_id, "Вы уже зарегестрированы")
        return
    
    send_message(chat_id, "Введите username и password через пробел")
    # set_status(user_id, 1)


def login(chat_id, user_id):
    if len(find_user(user_id)) == 0:
        send_message(chat_id, "Вы не зарегестрированы")
        return;
    send_message(chat_id, "Введите username password через пробел")
    set_status(user_id, 2)

def logout(chat_id, user_id):
    if get_login_status(user_id) == 0:
        send_message(chat_id, "Вы и так не авторизованы")
    else:
        set_login_status(user_id, 0) # status - login asked
        send_message(chat_id, "Выполнен выход")

def send_test(chat_id):
    words = get_random_words(4)
    msg = "Here are our words: {}".format(words)
    send_message(chat_id, msg)
    