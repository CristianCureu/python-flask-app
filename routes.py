from flask import render_template, request, redirect, url_for
from __init__ import app
from models import Users
from user_functions import login_user, register_user


@app.route("/")
@app.route("/<name>")
def hello_name(name=None):
    return render_template('hello.html', name=name)


@app.route("/users/")
def get_users():
    users = Users.query.all()
    print(f"{users}")
    return render_template("users.html", users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    response = {'error': False, 'message': None}
    # error = False
    if request.method == "POST":
        # print(f"Received POST request data: {request.form}")
        login_result = login_user(request.form['username'], request.form['password'])
        response = login_result
        if not response['error']:
            return redirect(url_for('hello_name', name=request.form['username']))
    return render_template('login.html', response=response)


@app.route('/register', methods=['POST', 'GET'])
def register():
    response = {'error': False, 'message': None} #valori initiale
    if request.method == 'POST':
        registration_result = (
            register_user(request.form['username'], request.form['password'], request.form['confirm_password']))
            #facem requestu din html
        response = registration_result #daca aplicam POST , valorile initiale se schimba
    return render_template('register.html', response=response) #dupa ce se termina IF-u,aratam pe UI


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

