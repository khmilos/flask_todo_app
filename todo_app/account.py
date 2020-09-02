from flask import (
    Blueprint, render_template, request
)

from todo_app.db import get_db


bp = Blueprint('account', __name__)


@bp.route('/registration', methods=('GET', 'POST'))
def registration():
    if request.method == 'POST':
        print(request)
    return render_template('account/registration.html')


@bp.route('/login')
def login():
    return render_template('account/login.html')


# @bp.route('/profile')
# def index():
#     db = get_db()
#     return render_template('account/profile.html')