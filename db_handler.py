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
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words(word_en, word_type) VALUES ('{}', '{}');".format(word.word_en, word.word_type))
    connection.commit()
    connection.close()

def find_word_id(word_en:str):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM words WHERE word_en='{}';".format(word_en))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]

def find_user(user_id):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res

def find_user(username, password):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE USERNAME='{}' AND PASSWORD='{}'".format(username, password))
    res = cursor.fetchall()
    connection.close()
    return res

def insert_meaning(meaning:Meaning):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meanings(word_id, meaning) VALUES ({}, '{}');".format(meaning.word_id, meaning.meaning))
    connection.commit()
    connection.close()

def insert_user(user:User):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(user_id, role, chat_id, status, login_status, username, password) VALUES ({}, '{}', {}, {}, {}, '{}', '{}');".\
        format(user.user_id, user.role, user.chat_id, user.status, user.login_status, user.username, user.password))
    connection.commit()
    connection.close()

def get_random_words(amount):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words ORDER BY rand() LIMIT {};".format(amount))
    res = cursor.fetchall()
    connection.close()
    return res

def set_status(user_id, status:int):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET status={} WHERE user_id={};".format(status, user_id))
    connection.commit()
    connection.close()

def get_status(user_id):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT status FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]

def set_login_status(user_id, login_status:int):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET login_status={} WHERE user_id={}".format(login_status, user_id))
    connection.commit()
    connection.close()

def get_login_status(user_id):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT login_status FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]

'''
def insert_login(login:Login):
    connection = create_connection(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO logins (username, password) VALUES ('{}', '{}');".format(login.username, login.password))
    connection.commit()
    connection.close()
'''