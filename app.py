import sqlalchemy
from telegram import replymarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from db_handler import *
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import telegram
from config import *
import logging
from req_commands import send_message
from bot_commands import *
from models import *
from telegram.ext import ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from flask_models import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    json_req = request.get_json()    
    update = telegram.Update.de_json(json_req, bot)
    chat_id = update.message.chat.id   
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    # try:            
    #     reply_keyboard = [["Option 1", "Option 2", "Option 3"]]
    #     bot.sendMessage(chat_id=chat_id, text="Hello, here are our options:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    # except Exception as e:
    #     bot.send_message(chat_id=chat_id, text=e.with_traceback)

    # bot.send_message(chat_id=chat_id, text="Removing reply keyboard", reply_markup=ReplyKeyboardRemove())
    
    if update.message.text is None:
        return "ok"


    text = update.message.text  

    user = find_user_by_id(user_id)
    send_message(chat_id, "Your entry in db:\ntype:{}\nuser:{}".format(type(user), user))
    send_message(chat_id, "Started checking status")
    if len(user) > 0:
        user_statuses = get_status(user_id)
        status = 0
        for elem in user_statuses:
            if elem[0] != 0:
                status = elem[0]
                break
        bot.send_message(chat_id=chat_id, text="Your status: {}".format(status))
        if status == 1:
            try:
                login_data = text.split()
                if len(login_data) < 2:
                    send_message(chat_id, "Вы неправильно ввели данные, попробуйте еще раз")
                else:
                    if len(find_user_by_data(login_data[0], user_id)) > 0:
                        send_message(chat_id, "Ошибка. У вас уже есть аккаунт с таким именем")
                    else:
                        update_user_data(user_id, "None", login_data[0], login_data[1])
                        update_user_status(user_id, login_data[0], 0)
                        update_user_login_status(user_id, login_data[0], 1)                    
                        send_message(chat_id, "Вы успешно зарегистрированы")
            except Exception:
                send_message(chat_id, "Упс, что то пошло не так")
            return "ok"
        if status == 2:
            try:
                pass
            except Exception:
                send_message(chat_id, "Упс, что то пошло не так")         
        if status == 3:
            pass   

    send_message(chat_id, "Ended checking status")

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
    elif text == "/logout":
        logout(chat_id, user_id)
    elif text == "/stats":
        pass
    elif text == "/test":
        send_test(chat_id)
    elif text == "/db":
        send_message(chat_id, "DB command recognized")
        users = read_users()
        users_str = ""
        for user in users:
            users_str += "{}\n".format(user)
        meanings = read_meanings()
        meanings_str = ""
        for meaning in meanings:
            meanings_str += "{}\n".format(meaning)
        words = read_words()
        words_str = ""
        for word in words:
            words_str += "{}\n".format(word)
        send_message(chat_id, "Users:\n{}".format(users_str))
        send_message(chat_id, "Words:\n{}".format(words_str))
        send_message(chat_id, "Meanings:\n{}".format(meanings_str))        
    else:
        bot.sendMessage(chat_id=chat_id, text="huh?")
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

@app.route("/createtables")
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)