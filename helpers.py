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
    """
    Get a database connection.
    
    If a connection is not yet established, establish a new one.
    
    Returns:
        SQLite database connection object.
    """
    
    # Check if 'g' (Flask application context) has '_sqlite_db' attribute
    # This attribute stores the database connection
    if not hasattr(g, '_sqlite_db'):
        # If not, establish a new database connection
        # The connection is created with the filename specified in the config module
        g._sqlite_db = sqlite3.connect(DATABASE_FILENAME)
        
        # Each row that is returned from the database using this connection
        # instead of a tuple will be a dictionary
        g._sqlite_db.row_factory = sqlite3.Row
    
    return g._sqlite_db


# Close connection to database
def close_connection(exception):
    """
    Close the database connection.

    This function is used as a teardown function by Flask's application context.
    It checks if there is a database connection and if so, closes it.

    Args:
        exception: The exception that occurred, if any. Unused in this function.
    """
    db = getattr(g, '_sqlite_db', None)
    if db is not None:
        # Get the '_sqlite_db' attribute from the Flask application context 'g'.
        # If it exists, close the database connection.
        db.close()


# Function to execute sql requests to get info from and to db
def execute_query(query, *query_args, one=False):
    """
    Executes a SQL query on the database and returns the result.

    Args:
        query (str): The SQL query to execute.
        query_args (tuple, optional): The parameters to substitute in the query. Defaults to ().
        one (bool, optional): If True, returns only the first row of the result. Defaults to False.

    Returns:
        The result of the SQL query. If the query is a SELECT statement, returns a single row as dict
        if one=True, otherwise returns all rows as list of dicts.
        If the query is a SELECT statement and returns no rows, returns None.
        If the query is an INSERT statement, returns the last inserted row id as integer.
        If it's any other type of statement, returns None.
    """
    # Establish a database connection if not already established
    db = get_db()
    
    # Create a cursor object to execute the query
    cursor = db.cursor()
    
    # Execute the SQL query
    cursor.execute(query, query_args)
    
    # Determine the type of query and return the appropriate result
    if query.split()[0].lower() == 'select':
        # If it's a SELECT statement, return one row if one=True, else return all rows
        result = cursor.fetchone() if one else cursor.fetchall()
        # If result is not empty, return it, otherwise return None
        if result:
            return result
        else:
            return None
    elif query.split()[0].lower() == 'insert':
        # If it's an INSERT statement, commit the changes and return the last inserted row id
        db.commit()
        return cursor.lastrowid
    else:
        # If it's any other type of statement, return None
        return None

    

