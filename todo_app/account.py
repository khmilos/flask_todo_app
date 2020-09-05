import os
import shutil
import uuid

from flask import (
    Blueprint, render_template, request, redirect, url_for, session, g, flash
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from werkzeug.utils import secure_filename

from todo_app.db import get_db


bp = Blueprint('account', __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()


@bp.route('/registration', methods=('GET', 'POST'))
def registration():
    if g.user is not None:
        return redirect(url_for('account.profile'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
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
                'INSERT INTO user(id, email, password, name) '
                'VALUES (?, ?, ?, ?)',
                (user_id, email, generate_password_hash(password), name)
            )

            cur_dir = os.curdir
            src_avatar = os.path.join(
                cur_dir, 
                'todo_app/static/default/avatar.jpg')
            dest_folder = os.path.join(cur_dir, 'todo_app/static/user')
            shutil.copy(src_avatar, dest_folder)
            dest_avatar = dest_folder + '/avatar.jpg'
            new_avatar = dest_folder + '/' + user_id + '.jpg'
            if os.path.isfile(new_avatar):
                os.remove(new_avatar)
            os.rename(dest_avatar, new_avatar)

            db.commit()
            session.clear()
            session['user_id'] = user_id
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('account/registration.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('account.profile'))

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


@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    if g.user is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        info = request.form['info']
        db = get_db()
        error = None

        if not info:
            error = 'Info is required.'

        if error is None:
            db.execute(
                'UPDATE user SET info = ? WHERE id = ?',
                (info, g.user['id'])
            )
            db.commit()
            return redirect(url_for('account.profile'))

        flash(error)

    return render_template('account/profile.html')


@bp.route('/profile/avatar', methods=('POST',))
def profile_avatar():
    if g.user is None:
        return redirect(url_for('index'))

    try:
        path = os.path.join(
            os.curdir, 
            'todo_app/static/user/' + g.user['id'] + '.jpg')

        if os.path.isfile(path):
            os.remove(path)

        f = request.files['img']
        f.save(path)
    except:
        flash('File uploading error.')

    return redirect(url_for('account.profile'))