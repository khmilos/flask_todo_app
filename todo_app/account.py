import uuid

from flask import (
    Blueprint, render_template, request, redirect, url_for, session, g, flash
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

from todo_app.db import get_db


bp = Blueprint('account', __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id # select


@bp.route('/registration', methods=('GET', 'POST'))
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', 
            (email,)
        ).fetchone() is not None:
            error = 'Email {} is already exists.'.format(email)

        if error is None:
            user_id = str(uuid.uuid4())
            db.execute(
                'INSERT INTO user(id, email, password) '
                'VALUES (?, ?, ?)',
                (user_id, email, generate_password_hash(password))
            )
            db.commit()
            session.clear()
            session['user_id'] = user_id
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('account/registration.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user = db.execute(
                'SELECT * FROM user WHERE email = ?',
                (email,)
            ).fetchone()
            
            if user is None:
                error = 'There are no such user.'
            elif not check_password_hash(user['password'], password):
                error = 'Wrong password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

        flash(error)

    return render_template('account/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# @bp.route('/profile')
# def index():
#     db = get_db()
#     return render_template('account/profile.html')