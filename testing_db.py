from db_commands import insert_user
from flask import Flask

from models import db, Account, User, account_user, Word, Meaning
from config import *
import admin_commands

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return "Homepage"

@app.route('/u')
def test_user():
    word_id = 65
    meanings = Meaning.query.filter_by(word_id=word_id).all()
    print(meanings)
    str = "Word\n"
    i = 1
    for elem in meanings:
        str += "{}. {}".format(i, elem.meaning)
        i += 1
    print(str)
    
    return "completed"

if __name__ == "__main__":
    app.run(debug=True)