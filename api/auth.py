import functools

from flask import (
    Blueprint, g, redirect, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from api.db import get_db

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
    username = request.json['username']
    password = request.json['password']
    db = get_db()

    if not username:
        return { 'error': 'Username is required' }

    if not password:
        return { 'error': 'Password is required' }

    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return { 'error': "User '" + username + "' is already registered." }

    return { 'success': "User '" + username + "' successfully registered." }

