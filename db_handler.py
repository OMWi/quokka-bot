import mysql.connector

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

class DB_handler:

    connection = None
    
    def __init__(self, host:str, db:str, user:str, password:str) -> None:
        self.hostname = host
        self.database = db
        self.user = user
        self.password = password

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.hostname, user=self.user,
                password=self.password, database=self.database 
            )
        except Exception as e:
            print(e.with_traceback)
        
        return connection
            

    
