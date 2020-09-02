import os

from flask import (Flask, render_template)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='SECRET',
        DATABASE=os.path.join(app.instance_path, 'todo_app.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('layout/index.html')

    from . import db
    db.init_app(app)

    from . import account
    app.register_blueprint(account.bp)

    return app