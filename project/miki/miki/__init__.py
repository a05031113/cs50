import os
from flask import Flask, redirect


def create_app(test_config=None):
    """
    Application Factory function
    """

    # Create app instance and configure it
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'miki.db'),
        SOURCE=os.path.join(app.instance_path, 'source/'),
        OUTPUT=os.path.join(app.instance_path, 'output/')
    )

    # App test_config is passed
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    # Make sure directories exist
    try:
        os.makedirs(app.config['SOURCE'])
        os.makedirs(app.config['OUTPUT'])
    except OSError:
        pass

    # Register database commands
    from miki import db
    db.register(app)

    # Register blueprints
    from miki import auth, edit
    app.register_blueprint(auth.bp)
    app.register_blueprint(edit.bp)

    # Return app instance
    return app
