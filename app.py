from db_handler import create_connection, find_user, get_status
import re
from flask import Flask, request
import requests
import telegram
import config
# import logging
from req_commands import send_message
from bot_commands import send_test, login, registrate

from models import *
import db_handler

# logging.basicConfig(level=logging.DEBUG)

words = []

bot = telegram.Bot(token=config.TOKEN)
# connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
app = Flask(__name__)

@app.route('/{}'.format(config.TOKEN), methods=['POST'])
def respond():
    json_req = request.get_json()
    
    update = telegram.Update.de_json(json_req, bot)

    chat_id = update.message.chat.id   
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    
    
    if update.message.text is None:
        return "ok"

    text = update.message.text  

    if len(find_user(user_id)) > 0:
        status = get_status(user_id)
        if status == 1:
            # something not right here
            try:
                login_data = text.split()
                newUser = User(user_id, "casual", chat_id, 0, 1, login_data[0], login_data[1])
                db_handler.insert_user(newUser)
            except Exception:
                send_message(chat_id, "Упс, что то пошло не так")
        if status == 2:
            try:
                user = find_user()
                pass
            except Exception:
                send_message(chat_id, "Упс, что то пошло не так")            


    if text == "/start":
        ans = "Привет {}. Quokka bot активирован.".format(user_name)
        send_message(chat_id, ans)
    elif text == "/about":
        ans = "Я Quokka Bot, создан для помощи в изучении английских слов"
        send_message(chat_id, ans)
    elif text == "/login":
        login(chat_id, user_id)
    elif text == "/registrate":
        registrate(chat_id, user_id)
    elif text == "/stats":
        pass
    elif text == "/test":
        send_test(chat_id)
    elif text == "/db":
        pass
    else:
        bot.sendMessage(chat_id=chat_id, text="huh?")
    return "ok"




@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    res = bot.setWebhook('{URL}{HOOK}'.format(URL=config.URL, HOOK=config.TOKEN))
    if res:
        return "webhook setup successful"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return "Quokka bot homepage"


if __name__ == '__main__':
    app.run()