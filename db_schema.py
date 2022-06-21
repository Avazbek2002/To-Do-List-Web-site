from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

db = SQLAlchemy()

# a model of a user for the database
class User (db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)

    def __init__ (self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password

# a model of s list for the database
class List (db.Model):
    __table_name__="lists"
    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    user_id = db.Column(db.Integer)
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class ListItem (db.Model):
    __table_name__="items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    list_id = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def __init__ (self, name, list_id, completed):
        self.name = name
        self.list_id = list_id
        self.completed = completed

def dbinit ():
    user_list = [User("Avazbek", "Isroilov", "Avaz", security.generate_password_hash("12345")), User("SaidAmirxon", "Musajonov", "Amir", security.generate_password_hash("45678")), User("Otabek", "Khursaboyev", "Otash",security.generate_password_hash("qwerty"))]
    db.session.add_all(user_list)

    # find the id of the umailser Avazbek
    avaz_id = User.query.filter_by(username="Avaz").first().id
    amir_id = User.query.filter_by(username="Amir").first().id

    all_lists = [
        List("Projects", avaz_id),
        List("Lectures", avaz_id),
        List("Parties", amir_id),
        List("Meetings", amir_id)
    ]
    db.session.add_all(all_lists)

    lectures_id = List.query.filter_by(name="Lectures").first().list_id
    projects_id = List.query.filter_by(name="Projects").first().list_id

    all_items = [
        ListItem("CS131", lectures_id, True),
        ListItem("CS139", lectures_id, False),
        ListItem("CS126", lectures_id, True),
        ListItem("Hurdle", projects_id, False),
        ListItem("Data Structures", projects_id, True)
    ]

    db.session.add_all(all_items)

    db.session.commit()
