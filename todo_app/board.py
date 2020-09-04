from flask import (
    Blueprint, g, render_template, request
)


bp = Blueprint('board', __name__)


@bp.route('/board', methods=('GET', 'POST'))
def board():
    if g.user is None:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('board/board.html')