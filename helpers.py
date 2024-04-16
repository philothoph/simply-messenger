from flask import g, redirect, session
from functools import wraps
import sqlite3

# Decorator to ensure user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Establish database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect('simply.db')
    return g.sqlite_db


# Close connection to database
def close_connection(exception):
    db = getattr(g, '_sqlite_db', None)
    if db is not None:
        db.close()