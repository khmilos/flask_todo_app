import uuid

from flask import (
    Blueprint, redirect, url_for, render_template, g, request
)

from todo_app.db import get_db


bp = Blueprint('task', __name__)


@bp.route('/task/<board_id>', methods=('GET', 'POST'))
def task(board_id):
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        db.execute(
            'INSERT INTO task'
            ' (id, board_id, owner_id, status, name, description)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (
                str(uuid.uuid4), 
                board_id, 
                g.user['id'], 
                'wait', 
                name, 
                description
            )
        )
        db.commit()
        return redirect(url_for('task.task', board_id=board_id))

    if request.method == 'GET':
        board_name = db.execute(
            'SELECT name FROM board WHERE id = ?', 
            (board_id,)
        ).fetchone()['name']
        task_list = db.execute(
            'SELECT * FROM task WHERE board_id = ?',
            (board_id,)
        ).fetchall()
        return render_template(
            'task/task.html', 
            board_name=board_name,
            task_list=task_list
        )