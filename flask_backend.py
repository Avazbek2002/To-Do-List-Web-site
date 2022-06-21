from flask import Flask, render_template, request, redirect, session
from werkzeug import security
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from db_schema import db, User, List, ListItem, dbinit
import re

app = Flask(__name__)
app.secret_key = 'My name is Avazbek'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()


#route to the index
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user_password']
        
        username_database = [k.username for k in User.query.all()]
        user = User.query.filter_by(username = username).first()
        if username in username_database and security.check_password_hash(user.password, password):
            session['username']=request.form['username']
            session['userid'] = user.id
            return redirect('/toDoList')
        else:
            return redirect('/badlogin')
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surename']
        username = request.form['username']
        hashed_password = security.generate_password_hash(request.form['user_password'])
        db.session.add(User(name, surname, username, hashed_password))
        db.session.commit()
    
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/toDoList', methods = ["POST", "GET"])
def toDoList():
    user_id = session['userid']
    lists = List.query.filter_by(user_id=user_id)

    if request.method == 'POST':
        session['list'] = request.form['list']
        nameItem = request.form['nameItem']
        list_id = List.query.filter_by(name = session['list'])[0].list_id
        db.session.add(ListItem(name = nameItem, list_id = list_id, completed = False))
        db.session.commit()
    dict = {}

    for l in lists:
        dict[l.name] = [lItem.name for lItem in ListItem.query.filter_by(list_id = l.list_id)]
    return render_template('toDoList.html', value = dict)

@app.route('/newlist', methods = ["POST", "GET"])
def newlist():
    if request.method == "POST":
       user_id = session['userid']
       name = request.form["name"]
       db.session.add(List(name, user_id))
       db.session.commit()
       return redirect('/toDoList')

    return render_template('newlist.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/badlogin')
def badlogin():
    return render_template('badlogin.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')