# c:/Users/Peter/Documents/Care-Home-4/app/login_check.py
from functools import wraps
from flask import session, redirect, url_for, flash
def login_required(user_mode=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' not in session or not session['logged_in']:
                flash('You need to be logged in to access this page.', 'amber')
                return redirect(url_for('login.login'))
            if user_mode and session.get('user_mode') != user_mode:
                flash('You do not have the required permissions to access this page.', 'amber')
                return redirect(url_for('login.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator