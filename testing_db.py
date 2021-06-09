from db_commands import insert_user
from flask import Flask

from models import db, User
from config import *

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
    u = User(1234, "role", 0)
    insert_user(u)
    return "Test user inserted"

@app.route('/allusers')
def select_users():
    users = User.query.all()
    print(users)
    return "cool"

@app.route('/finduser')
def find_user():
    user = User.query.filter_by(user_id = 123).first()
    print(user)
    print(type(user))
    return "user found and printed"


if __name__ == "__main__":
    app.run(debug=True)