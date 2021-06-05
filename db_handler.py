import mysql.connector
from models import *
import config

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

def find_user(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    return res

def insert_meaning(connection, meaning:Meaning):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meanings(word_id, meaning) VALUES ({}, '{}');".format(meaning.word_id, meaning.meaning))
    connection.commit()

def insert_user(user:User):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(user_id, role, chat_id, status, login_status) VALUES ({}, '{}', {}, {}, {});".\
        format(user.user_id, user.role, user.chat_id, user.status, user.login_status))
    connection.commit()
    connection.close()

def get_random_words(connection, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words ORDER BY rand() LIMIT {};".format(amount))
    res = cursor.fetchall()
    return res

def set_status(connection, user_id, status:int):
    cursor = connection.cursor()
    cursor.execute("UPDATE users PUT status={} WHERE user_id={};".format(status, user_id))
    connection.commit()

def set_login_status(connection, user_id, login_status:int):
    cursor = connection.cursor()
    cursor.execute("UPDATE users PUT login_status={} WHERE user_id={}".format(login_status, user_id))
    connection.commit()

def insert_login(connection, login:Login):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO logins (username, password) VALUES ('{}', '{}');".format(login.username, login.password))
    connection.commit()
