import functools

from flask import (
    Blueprint, g, redirect, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

# blueprint for authentication functions
bp = Blueprint('auth', __name__, url_prefix='/auth')

def find_user(email, include_password=False):
    user = get_db().execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()

    if not include_password:
      del(user['password']) # delete key from dictionary

    return user

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    db = get_db()

    if not email:
        return { 'status': 'error', 'message': 'Email is required' }

    if not password:
        return { 'status': 'error', 'message': 'Password is required' }

    try:
        db.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return {
            'status': 'error',
            'message': "Email '" + email + "' is already registered."
        }

    return {
        'status': 'success',
        'message': "Email '" + email + "' successfully registered.",
        'user': find_user(email)
    }

@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    db = get_db()

    user = find_user(email, True) # include password in dictionary

    if user is None:
        return { 'status': 'error', 'message': 'Incorrect email ' + email }
    elif not check_password_hash(user['password'], password):
        return { 'status': 'error', 'message': 'Incorrect password' }

    del(user['password']) # no password in response
    return {
        'status': 'success',
        'message': 'User authenticated',
        'user': user
    }

@bp.route('/users', methods=['GET'])
def users():
    db = get_db()

    users = db.execute('SELECT * FROM users').fetchall()

    if users is None:
        return { 'count': 0, 'status': 'error', 'message': 'No users registered' }

    user_list = []
    for user in users:
        user_list.append({
            'id': user['id'],
            'email': user['email'],
            'created_at': user['created_at']
        })

    return { 'users': user_list, 'count': len(users), 'success': 'Users fetched' }
