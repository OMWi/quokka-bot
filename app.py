from flask import Flask, request
import telegram
from telegram import ReplyKeyboardMarkup
import logging
import asyncio

from models import db, User, Account, Word, Meaning
from config import TOKEN, URL, DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USERNAME
from bot_commands import *
from admin_commands import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
with app.app_context():
    db.create_all()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def async_func(bot, user_id):
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        bot.send_message(chat_id=admin.user_id, text="User <{}> started registration".format(user_id))


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    json_req = request.get_json()    
    update = telegram.Update.de_json(json_req, bot)
    chat_id = update.message.chat.id   
    user_id = update.effective_user.id
    username = update.effective_user.first_name

    if update.message.text is None:
        bot.send_message(chat_id=chat_id, text="Что это такое!?")
        return "ok"
    
    text = update.message.text  
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter(Account.users.any(user_id=user_id)).filter_by(account_status=1).first()

    if user is not None:
        status = user.user_status
        if status == 0:
            pass
        elif status == 1:
            username = account.username
        elif status == 2:
            registrate_2(bot, chat_id, user_id, text)
            return "ok"
        elif status == 3:
            registrate_3(bot, chat_id, user_id, text)
            return "ok"
        elif status == 4:
            registrate_4(bot, chat_id, user_id, text)
            return "ok"
        elif status == 11:
            login_2(bot, chat_id, user_id, text)
            return "ok"
        elif status == 12:
            login_3(bot, chat_id, user_id, text)
            return "ok"

    if text == "/start":
        ans = "Привет {}. Quokka bot активирован.".format(username)
        bot.send_message(chat_id=chat_id, text=ans)
    elif text == "/about":
        ans = "Я Quokka Bot, создан для помощи в изучении английских слов"
        bot.send_message(chat_id=chat_id, text=ans)
    elif text == "/info":
        if user.user_status == 0:
            bot.send_message(chat_id=chat_id, text="Вы гость")
        elif user.user_status == 1:
            bot.send_message(chat_id=chat_id, text="Аккаунт:\nимя - {};\nпочта - {}".format(account.username, account.mail))
        elif 2 <= user.user_status <= 4:
            bot.send_message(chat_id=chat_id, text="Вы в процессе регистрации")
        elif 11 <= user.user_status <= 12:
            bot.send_message(chat_id=chat_id, text="Вы в процессе входа в аккаунт")
        elif 100 <= user.user_status <= 200:
            bot.send_message(chat_id=chat_id, text="Вы властелин смертных душ")
    elif text == "/login":
        login_1(bot, chat_id, user_id)
    elif text == "/register":
        loop.run_until_complete(async_func(bot, user_id))
        registrate_1(bot, chat_id, user_id)
    elif text == "/logout":
        logout(bot, chat_id, user_id)
    elif text == "/word":
        word(bot, chat_id, user_id)
    else:
        if user is not None and user.role == "admin":
            status = user.user_status
            if status == 100:
                insert_word_2(bot, chat_id, user_id, text)
                return "ok"
            elif status == 101:
                delete_word_2(bot, chat_id, user_id, text)
                return "ok"
            elif status == 110:
                insert_meaning_2(bot, chat_id, user_id, text)
                return "ok"
            elif status == 111:
                delete_meaning_2(bot, chat_id, user_id, text)
                return "ok"

            if status != 1:
                bot.send_message(chat_id=chat_id, text="huh?".format(text))
                return "ok"
            admin_keyboard = [
                ["Add new word", "Delete word", "Show all words"],
                ["Add new meaning", "Delete meaning", "Show all meanings"],
                ["Show all users", "Show all accounts"],
            ]
            if text == "/admin":                
                bot.send_message(chat_id=chat_id, text="Adming commands", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=False))
                return "ok"

            if text == admin_keyboard[0][0]:
                insert_word_1(bot, chat_id, user_id)
            elif text == admin_keyboard[0][1]:
                delete_word_1(bot, chat_id, user_id)
            elif text == admin_keyboard[0][2]:
                words = Word.query.all()
                str = "Words:\n"
                for elem in words:
                    str += elem.__str__() + "\n"
                bot.send_message(chat_id=chat_id, text = str)
            elif text == admin_keyboard[1][0]:
                insert_meaning_1(bot, chat_id, user_id)
            elif text == admin_keyboard[1][1]:
                delete_meaning_1(bot, chat_id, user_id)
            elif text == admin_keyboard[1][2]:
                meanings = Meaning.query.all()
                str = "Meanings:\n"
                for elem in meanings:
                    str += elem.__str__() + "\n"
                bot.send_message(chat_id=chat_id, text=str)
            elif text == admin_keyboard[2][0]:
                users = User.query.all()
                str = "Users:\n"
                for elem in users:
                    str += elem.__str__() + "\n"
                bot.send_message(chat_id=chat_id, text=str)
            elif text == admin_keyboard[2][1]:
                accounts = Account.query.all()
                str = "Accounts:\n"
                for elem in accounts:
                    str += elem.__str__() + "\n"
                bot.send_message(chat_id=chat_id, text=str)                
            else:
                bot.send_message(chat_id=chat_id, text="huh?")
        else:
            bot.send_message(chat_id=chat_id, text="Что, что?")
    return "ok"


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
