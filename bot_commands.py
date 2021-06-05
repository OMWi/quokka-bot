from req_commands import send_message
from db_handler import get_random_words, create_connection, find_user
from models import User
import config

def registrate(chat_id, user_id, conn):
    if len(find_user(conn, user_id)) == 0:
        send_message(chat_id, "Вы уже зарегестрированы")
        return
    
    send_message(chat_id, "Введите username и password через пробел")
    newUser = User(user_id, "casual", chat_id)


def login(chat_id, user_id):
    pass

def send_test(chat_id):
    conn = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    words = get_random_words(conn, 4)
    msg = "Here are our words: {}".format(words)
    send_message(chat_id, msg)
    