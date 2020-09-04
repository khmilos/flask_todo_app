import uuid

from flask import (
    Blueprint, g, render_template, request, redirect, url_for
)

from todo_app.db import get_db


bp = Blueprint('board', __name__)


@bp.route('/board', methods=('GET', 'POST', 'PUT'))
def board():
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        db.execute(
            'INSERT INTO board(id, owner_id, name) VALUES(?, ?, ?)',
            (str(uuid.uuid4()), g.user['id'], name)
        )
        db.commit()
        return redirect(url_for('board.board'))

    if request.method == 'GET':
        boardList = db.execute(
            'SELECT * FROM board WHERE owner_id = ?',
            (g.user['id'],)
        ).fetchall()

        return render_template('board/board.html', boardList=boardList)