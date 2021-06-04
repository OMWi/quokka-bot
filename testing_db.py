import db_handler
from models import *
from config import *

conn = db_handler.create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
res = db_handler.get_tables(conn)
print(res)