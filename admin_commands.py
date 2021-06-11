from models import db, User, Account, Word, Meaning

# words
def insert_word_1(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    user.user_status = 100
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Введите английское слово и его тип через пробел")

def insert_word_2(bot, chat_id, user_id, text):
    user = User.query.filter_by(user_id=user_id).first()
    words_arr = text.split()
    if len(words_arr) < 2:
        bot.send_message(chat_id=chat_id, text="Неправильный ввод")
        user.user_status = 1
        return 

    user.user_status = 1
    word_en = ""
    for i in range(len(words_arr)-1):
        word_en += words_arr[i] + " "
    new_word = Word(word_en, words_arr[-1])
    db.session.add(new_word)
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Слово '{}' добавлено".format(word_en))  

def delete_word_1(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    user.user_status = 101
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Введите id слова для удаления")

def delete_word_2(bot, chat_id, user_id, text):
    user = User.query.filter_by(user_id=user_id).first()
    id = -1
    try:
        id = int(text)
    except Exception:
        bot.send_message(chat_id=chat_id, text="Неправильный ввод")
        user.user_status = 1
        db.session.commit()
        return
    
    word = Word.query.filter_by(id=id).first()
    if word is None:
        bot.send_message(chat_id=chat_id, text="Слово не найдено")
        user.user_status = 1
        db.session.commit()
    else:
        meanings = Meaning.query.filter_by(word_id=id).all()
        for elem in meanings:
            db.session.delete(elem)
        word_en = word.word_en
        db.session.delete(word)
        user.user_status = 1
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Слово {} удалено".format(word_en))

# meanings

def insert_meaning_1(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    user.user_status = 110
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Введите слово и значение через пробел")

def insert_meaning_2(bot, chat_id, user_id, text):    
    user = User.query.filter_by(user_id=user_id).first()
    arr = text.split()
    if len(arr) < 2:
        bot.send_message(chat_id=chat_id, text="Неправильный ввод")
        user.user_status = 1
        return
    word = Word.query.filter_by(word_en=arr[0]).first()
    if word is None:
        bot.send_message(chat_id=chat_id, text="Слово не найдено")
        user.user_status = 1
        db.session.commit()
        return

    user.user_status = 1
    meaning = ""
    for i in range(1, len(arr)):
        meaning += arr[i] + " "
    new_meaning = Meaning(meaning, word.id)
    db.session.add(new_meaning)
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Определение: {}\nДобавлено".format(meaning))   


def delete_meaning_1(bot, chat_id, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    user.user_status = 111
    db.session.commit()
    bot.send_message(chat_id=chat_id, text="Введите id определения для удаления")

def delete_meaning_2(bot, chat_id, user_id, text):
    user = User.query.filter_by(user_id=user_id).first()
    id = -1
    try:
        id = int(text)
    except Exception:
        bot.send_message(chat_id=chat_id, text="Неправильный ввод")
        user.user_status = 1
        db.session.commit()
        return
    
    meaning = Meaning.query.filter_by(id=id).first()
    if meaning is None:
        bot.send_message(chat_id=chat_id, text="Определение не найдено")
        user.user_status = 1
        db.session.commit()
    else:
        meaning_text = meaning.meaning
        db.session.delete(meaning)
        user.user_status = 1
        db.session.commit()
        bot.send_message(chat_id=chat_id, text="Определение: \n{}\nУдалено".format(meaning_text))

