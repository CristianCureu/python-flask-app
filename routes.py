from flask import render_template, request, redirect, url_for, session
from main import app
from models import User
from user_functions import login_user, register_user


@app.route("/")
def main_page():
    username = session.get("username")
    return render_template('main.html', username=username)


@app.route("/users")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    response = {'error': False, 'message': None}
    if request.method == "POST":
        login_result = login_user(request.form['username'], request.form['password'])
        response = login_result
        if not response['error']:
            return redirect(url_for('main_page', name=request.form['username']))
    return render_template('login.html', response=response)


@app.route('/register', methods=['POST', 'GET'])
def register():
    response = {'error': False, 'message': None}
    print("a")
    if request.method == 'POST':
        registration_result = (
            register_user(request.form['username'], request.form['password'], request.form['confirm_password']))
        response = registration_result
    return render_template('register.html', response=response)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main_page'))


@app.route('/logs')
def get_logs():
    try:
        file_path = "data/logs.txt"
        lines = []
        with open(file_path, 'r') as file:
            for line in file:
                lines.append(line.strip())
        return render_template('logs.html', lines=lines)
    except FileNotFoundError:
        return "File not found"

