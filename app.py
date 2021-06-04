import re
from flask import Flask, request
import requests
import telegram
import config
# import logging
from req_commands import send_message, send_test

# logging.basicConfig(level=logging.DEBUG)

bot = telegram.Bot(token=config.TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(config.TOKEN), methods=['POST'])
def respond():
    json_req = request.get_json()
    
    update = telegram.Update.de_json(json_req, bot)

    chat_id = update.message.chat.id   
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    
    send_message(chat_id, json_req)
    ans = "Type of your user_id {}. user_id {}.".format(type(user_id), user_id)
    send_message(chat_id, ans)
    
    if update.message.text is None:
        return "ok"

    text = update.message.text    

    if text == "/start":
        ans = "Привет {}. Quokka bot активирован.".format(user_name)
        send_message(chat_id, ans)
    elif text == "/about":
        ans = "Я Quokka Bot, создан для помощи в изучении английских слов"
        send_message(chat_id, ans)
    elif text == "/login":
        pass
    elif text == "/register":
        pass
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