from databases import *
import os
from flask import Flask, request, redirect, render_template
from flask import session as login_session
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'

UPLOAD_FOLDER = '/home/student/Documents/y2s19-flask-login/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/login', methods=['POST'])
def login():
    user = get_user(request.form['username'])
    if user != None and user.verify_password(request.form["password"]):
        login_session['name'] = user.username
        login_session['logged_in'] = True
        return logged_in()
    else:
        return home()


@app.route('/signup', methods=['POST'])
def signup():
    #check that username isn't already taken
    user = get_user(request.form['username'])
    if user == None:
        add_user(request.form['username'],request.form['password'])
    return home()


@app.route('/logged-in', methods=['GET', 'POST'])
def logged_in():
    if request.method == 'POST':
        try:
            edit_food(login_session['name'], request.form['food'])
        except KeyError as e:
            pass
    user = get_user(login_session['name'])
    return render_template('logged.html', food=user.fav_food, path=user.pic_path)


@app.route('/logout')
def logout():
    login_session['name'] = None
    login_session['logged_in'] = False
    return home()


@app.route('/upload', methods = ['POST'])
def upload_pic():
    f = request.files['pic']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
    edit_path(login_session['name'], f.filename)
    return logged_in()

if __name__ == '__main__':
    app.run(debug=True)
