import uuid

from flask import (
    Blueprint, redirect, url_for, render_template, g, request
)

from todo_app.db import get_db


bp = Blueprint('task', __name__)


@bp.route('/task/<board_id>', methods=('GET', 'POST', 'PUT'))
def task(board_id):
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        db.execute(
            'INSERT INTO task'
            ' (id, board_id, status, name, description)'
            ' VALUES (?, ?, ?, ?, ?)',
            (
                str(uuid.uuid4()), 
                board_id, 
                'wait', 
                name, 
                description
            )
        )
        db.commit()
        return redirect(url_for('task.task', board_id=board_id))

    if request.method == 'GET':
        board = db.execute(
            'SELECT id, name FROM board WHERE id = ?', 
            (board_id,)
        ).fetchone()
        task_list = db.execute(
            'SELECT * FROM task WHERE board_id = ?',
            (board_id,)
        ).fetchall()
        return render_template(
            'task/task.html', 
            board=board,
            task_list=task_list
        )


@bp.route('/task/<board_id>/change/<task_id>', methods=('POST',))
def task_change(board_id, task_id):
    if g.user is None:
        return redirect(url_for('index'))
    
    name = request.form['name']
    status = request.form['status']
    description = request.form['description']

    db = get_db()
    db.execute(
        'UPDATE task SET name = ?, status = ?, description = ?'
        ' WHERE id = ?',
        (name, status, description, task_id)
    )
    db.commit()
    return redirect(url_for('task.task', board_id=board_id))


@bp.route('/task/<board_id>/delete/<task_id>', methods=('POST',))
def task_delete(board_id, task_id):
    if g.user is None:
        return redirect(url_for('index'))

    db = get_db()
    db.execute(
        'DELETE FROM task WHERE id = ?',
        (task_id,))
    db.commit()
    return redirect(url_for('task.task', board_id=board_id))