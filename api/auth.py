import functools

from flask import (
    Blueprint, g, redirect, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

# blueprint for authentication functions
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method != 'POST':
        return { 'error': 'POST method required' }

    email = request.json['email']
    password = request.json['password']
    db = get_db()

    if not email:
        return { 'error': 'Email is required' }

    if not password:
        return { 'error': 'Password is required' }

    try:
        db.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return { 'error': "Email '" + email + "' is already registered." }

    return { 'success': "Email '" + email + "' successfully registered." }

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method != 'POST':
        return { 'error': 'POST method required' }

    email = request.json['email']
    password = request.json['password']
    db = get_db()

    user = db.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()

    if user is None:
        return { 'error': 'Incorrect email ' + email }
    elif not check_password_hash(user['password'], password):
        return { 'error': 'Incorrect password' }

    return { 'success': 'User authenticated' }

@bp.route('/users', methods=('GET', 'POST'))
def users():
    if request.method == 'POST':
        return { 'error': 'GET method required' }

    db = get_db()

    users = db.execute('SELECT * FROM users').fetchall()

    if users is None:
        return { 'count': 0, 'error': 'No users registered' }

    #for user in users:
    user_list = []
    for user in users:
      user_list.append({
        'email': user['email'],
        'created_at': user['created_at']
      })

    return { 'users': user_list, 'count': len(users), 'success': 'Users fetched' }

