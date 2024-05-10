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
def execute_query(sql_query, *query_params, one=False):
    """
    Executes a SQL query on the database and returns the result.

    Args:
        sql_query (str): The SQL query to execute.
        query_params (tuple, optional): The parameters to substitute in the query.
        return_one (bool, optional): If True, returns only the first row of the result.

    Returns:
        The result of the SQL query:
        - For SELECT statements, a single row as a dictionary if one=True,
          else a list of dictionaries. If no rows, returns None.
        - For INSERT, UPDATE or DELETE statements, the number of rows affected
        - For other statements, None.
    """
    # Get the database connection
    db = get_db()
    
    # Create a cursor for the database connection
    cursor = db.cursor()
    
    # Execute the SQL query
    cursor.execute(sql_query, query_params)
    
    # Initialize the result variable
    result = None
    
    # Check the type of the SQL query
    if sql_query.split()[0].lower() == 'select':
        # If it's a SELECT statement, get the result
        result = cursor.fetchone() if one else cursor.fetchall()
        if not result:
            result = None
    elif sql_query.split()[0].lower() in ('insert', 'update', 'delete'):
        # If it's an INSERT, UPDATE or DELETE statement, commit changes
        db.commit()
        # Get the number of rows affected
        result = cursor.rowcount

    return result
