from db_handler import create_connection
import re
from flask import Flask, request
import requests
import telegram
import config
# import logging
from req_commands import send_message
from bot_commands import send_test, login   

from models import *
import db_handler

# logging.basicConfig(level=logging.DEBUG)

words = []

bot = telegram.Bot(token=config.TOKEN)
connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
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

    if text == "/admin":
        admin = User(user_id, "admin", chat_id, 0, 1, "omwi", "67936793")
        db_handler.insert_user(connection, admin)
        ans = "Вы становитесь админом"
        send_message(chat_id, ans)
        return "ok"  

    if text == "/start":
        ans = "Привет {}. Quokka bot активирован.".format(user_name)
        send_message(chat_id, ans)
    elif text == "/about":
        ans = "Я Quokka Bot, создан для помощи в изучении английских слов"
        send_message(chat_id, ans)
    elif text == "/login":
        login(chat_id)
        pass
    elif text == "/register":
        pass
    elif text == "/stats":
        pass
    elif text == "/test":
        global words
        words = send_test(chat_id)
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