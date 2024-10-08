from flask import Flask, render_template, request, redirect, url_for, flash, session
from backend import Backend


app = Flask(__name__, template_folder='../HTML', static_folder='../static')
backend = Backend('data.txt')
backend.parse_file()
app.secret_key = "HEY"

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if backend.login_checker(username, password):
            session['username'] = username
            return redirect(url_for('friend_list'))
        return render_template("login.html")
    return render_template("login.html")

@app.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        print(name,username,password)
        if backend.add_user(name,username,password):
            session['username'] = username
            return redirect(url_for('profile_page'))
        return render_template("sign_up.html")
    return render_template("sign_up.html")

@app.route("/friend_list")
def friend_list():
    username = session['username']
    me = backend.find_username(username)
    friend = me.online_friends()
    name = me.get_name()
    return render_template("friend_list.html", friend_list=friend, name=name)
    
@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/profile_page", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        ics_link = request.form['ics']
        username = session['username']
        me = backend.find_username(username)
        username = me.change_ics(ics_link)
        backend.save_file()
    username = session['username']
    return render_template("profile_page.html", username=username)

@app.route("/sign_out")
def sign_out():
    session.pop('username', default=None)

@app.route("/add_friend", methods=["POST"])
def add_friend():
    if request.method == "POST":
        username = session['username']
        me = backend.find_username(username)
        friend_name = request.form['friend_name']
        friend = backend.identity(friend_name)
        print(friend)
        if friend is None:
            return False
        if me.add_friend(friend):
            backend.save_file()
            return redirect(url_for('friend_list'))
        return False
