from flask import Flask, request
import telegram
import logging

from models import db, User, Account, Word, Meaning
from config import TOKEN, 
from bot_commands import 

# from telegram import replymarkup
# from telegram.replykeyboardremove import ReplyKeyboardRemove
# from telegram.ext import ConversationHandler, MessageHandler, Filters
# from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
with app.app_context():
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


    new_user = User(1, 2, "3", 4, 5)
    bot.send_message(chat_id=chat_id, text="Adding test new user")
    db_commands.insert_user(new_user)  
    
    text = update.message.text  

    user = find_user_by_id(user_id)
    bot.send_message(chat_id=chat_id, text="Your entry in db:\ntype:{}\nuser:{}".format(type(user), user))
    bot.send_message(chat_id=chat_id, text="Started checking status")
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
                    bot.send_message(chat_id=chat_id, text="Вы неправильно ввели данные, попробуйте еще раз")
                else:
                    if len(find_user_by_data(login_data[0], user_id)) > 0:
                        bot.send_message(chat_id=chat_id, text="Ошибка. У вас уже есть аккаунт с таким именем")
                    else:
                        update_user_data(user_id, "None", login_data[0], login_data[1])
                        update_user_status(user_id, login_data[0], 0)
                        update_user_login_status(user_id, login_data[0], 1)                    
                        bot.send_message(chat_id=chat_id, text="Вы успешно зарегистрированы")
            except Exception:
                bot.send_message(chat_id=chat_id, text="Упс, что то пошло не так")
            return "ok"
        if status == 2:
            try:
                pass
            except Exception:
                bot.send_message(chat_id=chat_id, text="Упс, что то пошло не так")         
        if status == 3:
            pass   

    bot.send_message(chat_id=chat_id, text="Ended checking status")

    if text == "/start":
        ans = "Привет {}. Quokka bot активирован.".format(user_name)
        bot.send_message(chat_id=chat_id, text=ans)
    elif text == "/about":
        ans = "Я Quokka Bot, создан для помощи в изучении английских слов"
        bot.send_message(chat_id=chat_id, text=ans)
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
        bot.send_message(chat_id=chat_id, text="DB command recognized")
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
        bot.send_message(chat_id=chat_id, text="Users:\n{}".format(users_str))
        bot.send_message(chat_id=chat_id, text="Words:\n{}".format(words_str))
        bot.send_message(chat_id=chat_id, text="Meanings:\n{}".format(meanings_str))        
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

if __name__ == '__main__':
    app.run()