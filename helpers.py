from config import DATABASE_FILENAME
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
    if not hasattr(g, '_sqlite_db'):
        g._sqlite_db = sqlite3.connect(DATABASE_FILENAME)
    return g._sqlite_db


# Close connection to database
def close_connection(exception):
    db = getattr(g, '_sqlite_db', None)
    if db is not None:
        db.close()


# Insert user to database
def insert_user(username, hash):
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, hash))
    db.commit()


# Function to execute sql requests to get info from db
def execute(req, *vars, one=False):
    db = get_db()
    cur = db.cursor()
    cur.execute(req, vars)
    res = cur.fetchone() if one else cur.fetchall()
    return res

