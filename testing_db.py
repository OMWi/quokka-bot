import db_handler
from models import *
from config import *

conn = db_handler.create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)

while True:
    '''
    word_en = input()
    word_type = input()
    newWord = Word(word_en, word_type)
    db_handler.insert_word(conn, newWord)
    print("{} inserted".format(word_en))
    '''
    '''
    word_en = input("word_en:")    
    meaning = input("meaning:")
    word_id = db_handler.find_word_id(conn, "admit")
    newMeaning = Meaning(meaning, word_id)
    db_handler.insert_meaning(conn, newMeaning)
    print("meaning {} inserted".format(meaning))
    '''
    '''
    res = db_handler.get_random_words(conn, 4)
    print(res)
    '''

    break