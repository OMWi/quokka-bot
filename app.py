from flask import Flask, request
import telegram
import config
import logging

logging.basicConfig(level=logging.DEBUG)

bot = telegram.Bot(token=config.TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(config.TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id   
    user_name = update.effective_user.first_name

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    if text == "/start":
        welcome_msg = "Hi, {}. {} now can talk with you.".format(user_name, config.BOT_USERNAME)
        bot.send_message(chat_id=chat_id, text=welcome_msg)
        # authorisation
    elif text == "/help":
        pass
    elif text == "/user":
        pass
    elif text == "/stats":
        pass
    elif text == "/test":
        # some magic
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