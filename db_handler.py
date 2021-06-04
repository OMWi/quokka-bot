import mysql.connector
from models import *

# todo: fix varchar lens here  

TABLES = {}
TABLES["words"] = (
    "CREATE TABLE 'words' ("
    "  'id' int unsigned not null auto_increment,"
    "  'word_en' varchar(20) not null,"
    "  'word_type' varchar(4) not null,"
    "  'primary key (id));"
)

TABLES["meanings"] = (
    "CREATE TABLE 'words' ("
    "  'id' int unsigned not null auto_increment,"
    "  'word_id' int unsigned not null,"
    "  'meaning' varchar(256) not null,"
    "  primary key (id),"
    "  foreign key (word_id) references words(id));"
)

TABLES["users"] = (
    "CREATE TABLE 'words' ("
    "  'id' int unsigned not null auto_increment,"
    "  'user_id' varchar(20) not null,"
    "  'role' varchar(16) not null,"
    "  'primary key (id));"
)


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

def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    res = cursor.fetchall()
    return res

def get_words(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words;")
    res = cursor.fetchall()
    return res

def describe_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE {};".format(table_name))
    res = cursor.fetchall()
    return res

def insert_word(connection, word:Word):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words(word_en, word_type) VALUES ('{}', '{}');".format(word.word_en, word.word_type))
    cursor.commit()


    
    
            

    
