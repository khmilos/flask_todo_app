import uuid

from flask import (
    Blueprint, g, render_template, request, redirect, url_for
)

from todo_app.db import get_db


bp = Blueprint('board', __name__)


@bp.route('/board', methods=('GET', 'POST'))
def board():
    if g.user is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        db = get_db()
        name = request.form['name']
        db.execute(
            'INSERT INTO board(id, owner_id, name) VALUES(?, ?, ?)',
            (str(uuid.uuid4()), g.user['id'], name)
        )
        db.commit()
        return redirect(url_for('board.board'))

    if request.method == 'GET':
        db = get_db()
        boardList = db.execute(
            'SELECT * FROM board WHERE owner_id = ?',
            (g.user['id'],)
        ).fetchall()

        return render_template('board/board.html', boardList=boardList)