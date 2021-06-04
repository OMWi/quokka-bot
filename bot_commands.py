from req_commands import send_message
from db_handler import get_random_words, create_connection
import config

def registrate(chat_id):
    send_message(chat_id, "Введите username и password через пароль")

def send_test(chat_id):
    conn = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    words = get_random_words(conn, 4)
    msg = "Here are our words: {}".format(words)
    send_message(chat_id, msg)
    