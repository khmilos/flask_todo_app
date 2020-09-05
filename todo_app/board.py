import uuid
import os
import shutil

from flask import (
    Blueprint, g, render_template, request, redirect, url_for
)

from todo_app.db import get_db


bp = Blueprint('board', __name__)


@bp.route('/board', methods=('GET', 'POST'))
def board():
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        board_id = str(uuid.uuid4())
        db.execute(
            'INSERT INTO board(id, owner_id, name) VALUES(?, ?, ?)',
            (board_id, g.user['id'], name)
        )

        cur_dir = os.curdir
        src_avatar = os.path.join(
            cur_dir, 
            'todo_app/static/default/board.jpg')
        dest_folder = os.path.join(cur_dir, 'todo_app/static/user')
        shutil.copy(src_avatar, dest_folder)
        dest_avatar = dest_folder + '/board.jpg'
        new_avatar = dest_folder + '/' + board_id + '.jpg'
        if os.path.isfile(new_avatar):
            os.remove(new_avatar)
        os.rename(dest_avatar, new_avatar)
        
        db.commit()
        return redirect(url_for('board.board'))

    if request.method == 'GET':
        board_list = db.execute(
            'SELECT * FROM board WHERE owner_id = ?',
            (g.user['id'],)
        ).fetchall()

        return render_template('board/board.html', board_list=board_list)


@bp.route('/change/<board_id>', methods=('POST',))
def board_change(board_id):
    if g.user is None:
        return redirect(url_for('index'))

    name = request.form['name']
    db = get_db()
    db.execute(
        'UPDATE board SET name = ? WHERE id = ?',
        (name, board_id)
    )
    db.commit()
    return redirect(url_for('board.board'))


@bp.route('/delete/<board_id>', methods=('POST',))
def board_delete(board_id):
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()
    db.execute(
        'DELETE FROM board WHERE id = ?',
        (board_id,)
    )
    db.commit()
    return redirect(url_for('board.board'))