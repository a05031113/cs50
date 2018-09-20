import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from miki.db import connect


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """Decorator for login"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Load user id from session"""
    # Gets user id from session
    user_id = session.get('user_id')

    # Checks if user id is empty
    if user_id is None:
        g.user = None
    else:
        # Gets username from database using id
        g.user = connect().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user"""
    # Forets user in current session
    session.clear()
    g.user = None

    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = connect()
        error = None

        # Check if parameters exist
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # Check if connection to database exist
        elif not db:
            error = 'Cannot connect to database.'
        # Query database for username
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone():
            error = 'User {} is already registered.'.format(username)

        # Registers user
        if error is None:
            # Add user in database
            db.execute(
                'INSERT INTO user (username, hash) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        # Flash error
        flash(error)

    # Serve register page
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in user"""
    # Forget user id if exists
    session.clear()
    g.user = None

    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = connect()
        error = None

        # Check if parameters exist in request
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not db:
            error = 'Cannot connect to database.'

        # Ugly code, could have been simpler if
        # assignment in conditonal clause were allowed
        if not error:
            # Query the database for user
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            # Check if username and password are correct
            if not user:
                error = 'Incorrect username.'
            elif not check_password_hash(user['hash'], password):
                error = 'Incorrect password.'

            # Logs in user
            if not error:
                session.clear()
                session['user_id'] = user['id']
                return redirect('/')

        # Flash error
        flash(error)

    # Server login page
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Log out user"""
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    """Reset password for user"""
    if request.method == 'POST':
        current_password = request.form.get('current-password', None)
        new_password = request.form.get('new-password', None)
        new_password_confirm = request.form.get('new-password-confirm', None)
        db = connect()
        error = None

        # Checks if parameters exist in request
        if not current_password:
            error = 'Current Password is required.'
        elif not new_password:
            error = 'New Password is required.'
        elif not new_password == new_password_confirm:
            error = 'New Passwords do not match.'

        # Checks if connection to database exist
        elif not db:
            error = 'Cannot connect to database.'
        # Checks if current password matches the hash in database
        elif not check_password_hash(g.user['hash'], current_password):
            error = 'Invalid password.'

        # Updates password in database
        if not error:
            db.execute(
                'UPDATE user SET hash = ? WHERE id = ?',
                (generate_password_hash(new_password), g.user['id'])
            )
            db.commit()

            # Redirects to login page
            return redirect(url_for('auth.login'))

        # Flash error
        flash(error)

    return render_template('auth/reset.html')
