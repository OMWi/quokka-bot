from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)


   chat_id = update.message.chat.id
   msg_id = update.message.message_id
   user_name = update.effective_user.first_name

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   
   if text == "/start":
       bot_welcome = "Hi, " + user_name
       bot.sendMessage(chat_id=chat_id, text=bot_welcome)

   return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    res = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if res:
        return "webhook setup successful"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return "Quokka bot homepage"


if __name__ == '__main__':
    app.run()