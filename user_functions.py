from models import User
from sqlalchemy.exc import IntegrityError
from main import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'error': True, 'message': "This user doesn't exist!"}
    elif not check_password_hash(user.password, password):
        return {'error': True, 'message': "Incorrect password!"}
    else:
        session['user_id'] = user.id
        session['username'] = user.username
        return {'error': False, 'message': "Login successful!"}


def register_user(username, password, confirm_password):
    if not len(username) >= 3:
        return {'error': True, 'message': 'Username must be at least 3 characters'}
    if not password == confirm_password:
        return {'error': True, 'message': 'Passwords must match!'}
    elif not len(password) >= 3:
        return {'error': True, 'message': 'Password must be at least 3 characters'}

    user = User.query.filter_by(username=username).first()
    if user:
        return {'error': True, 'message': 'Username already exists'}

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'error': False, 'message': 'Successfully registered!'}
    except IntegrityError:
        db.session.rollback()
        return {'error': True, 'message': 'Username already exists'}
