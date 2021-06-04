import mysql.connector
from models import *

def create_connection(hostname:str, user:str, password:str, database:str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname, user=user,
            password=password, database=database 
        )
    except Exception as e:
        print(e.with_traceback)
                
    return connection

def insert_word(connection, word:Word):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words(word_en, word_type) VALUES ('{}', '{}');".format(word.word_en, word.word_type))
    connection.commit()

def find_word_id(connection, word_en:str):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM words WHERE word_en='{}';".format(word_en))
    res = cursor.fetchall()
    return res[0][0]

def insert_meaning(connection, meaning:Meaning):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meanings(word_id, meaning) VALUES ({}, '{}');".format(meaning.word_id, meaning.meaning))
    connection.commit()

def insert_user(connection, user:User):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(user_id, role, chat_id, status) VALUES ({}, '{}', {}, {});".format(user.user_id, user.role, user.chat_id, user.status))
    connection.commit()

def get_random_words(connection, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words ORDER BY rand() LIMIT {}".format(amount))
    res = cursor.fetchall()
    return res
