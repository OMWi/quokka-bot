import re
from flask import Flask, request
import requests
import telegram
import config
import logging
import json

logging.basicConfig(level=logging.DEBUG)

bot = telegram.Bot(token=config.TOKEN)

app = Flask(__name__)

def send_message(chat_id, text):
    method = "sendMessage"
    url = "{tg_api}{token}/{method}".format(tg_api=config.TG_API, token=config.TOKEN, method=method)
    data = {"chat_id" : chat_id, "text" : text}
    requests.post(url, data=data)

@app.route('/{}'.format(config.TOKEN), methods=['POST'])
def respond():
    json_req = request.get_json()
    
    update = telegram.Update.de_json(json_req, bot)

    chat_id = update.message.chat.id   
    user_name = update.effective_user.first_name
    
    send_message(chat_id, json_req)
    
    if "text" not in json_req.keys():
        return ""
    text = update.message.text    

    if text == "/start":
        welcome_msg = "Hi, {}. {} now can talk with you.".format(user_name, config.BOT_USERNAME)
        bot.send_message(chat_id=chat_id, text=welcome_msg)
        # authorisation
    elif text == "/about":
        pass
    elif text == "/user":
        pass
    elif text == "/stats":
        pass
    elif text == "/test":
        # some magic
        pass
    elif text == "/db":
        pass
    else:
        bot.sendMessage(chat_id=chat_id, text="huh?")

    return ''




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