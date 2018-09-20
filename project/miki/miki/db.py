import click
from flask import current_app, g
from flask.cli import with_appcontext
import sqlite3


def connect():
    """
    Create connection to the database
    """

    # Checks if db exists in g
    if 'db' not in g:
        # Creats connection to database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    # Returns database
    return g.db


def disconnect(e=None):
    """
    Close connection from the database
    """
    # Pops out database connection from g
    db = g.pop('db', None)

    # If connection exists, closes it
    if db is not None:
        db.close()


def init():
    """
    Create tables from schema
    """

    # Connects to database
    db = connect()

    # Create tables define in schema.sql
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_command():
    """
    Command to initialize database
    """
    # Initialize database
    init()
    click.echo('Initialized the database.')


def register(app):
    """
    Register database functions to app instance
    """
    app.teardown_appcontext(disconnect)
    app.cli.add_command(init_command)
