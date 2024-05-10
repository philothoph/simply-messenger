from flask import Flask, flash, jsonify, render_template, redirect, request, session
from flask_session import Session
from helpers import close_connection, execute_query, login_required
from re import match
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
@login_required
def index():
    ''' Show contacts list with number of new messages '''

    # Get list of contacts with whom logged-in user has exchanged messages 
    contacts = execute_query('''
                             SELECT username FROM users WHERE id IN 
                             (SELECT sender_id FROM messages WHERE recipient_id = ?
                             UNION
                             SELECT recipient_id FROM messages WHERE sender_id = ?)
                             ''', session['user_id'], session['user_id'])
    
    # Count the number of new messages for each contact
    new_messages = execute_query('''
                                SELECT users.username, COUNT(*) AS count FROM messages
                                JOIN users ON users.id = sender_id
                                WHERE recipient_id = ? AND seen = 0
                                GROUP BY sender_id
                                ''', session['user_id'])   

    # Convert Row objects to list of dictionaries
    contacts = [dict(row) for row in contacts] if contacts else []                        
    
    # Convert Row objects to list of dictionaries
    new_messages = [dict(row) for row in new_messages] if new_messages else []
    
    # Add new_messages to dict_contacts
    for contact in contacts:
        for new_message in new_messages:
            if contact['username'] == new_message['username']:
                contact['new_messages'] = new_message['count']
    
    return render_template('index.html', contacts=contacts)
    

@app.route('/chat')
@login_required
def chat():
    ''' Chat with user '''

    # Get the username from the request arguments
    name = request.args.get('name')
    
    # Get the user's id from the database
    recipient_id = execute_query(
        'SELECT id FROM users WHERE username = ?', 
        request.args.get('name'), one=True)
    
    # If a user is found, get the id
    if recipient_id:
        recipient_id = recipient_id['id']
    else:
        # If a user is not found, redirect to index and return error message
        if name:
            flash('User ' + name + ' not found')
        return redirect('/')
    
    return render_template('chat.html', name=name, recipient_id=recipient_id)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    ''' Log user in '''

    # Forget user_id
    session.clear()

    # If user reached route via sending username and password
    if request.method == 'POST':
        # Check username
        username = request.form.get('username')
        if not username:
            return render_template('login.html', error='Please enter a username')
        if not execute_query('SELECT id FROM users WHERE username = ?', username, one=True):
            return render_template('login.html', error='Username or password is incorrect')
    
        # Check password
        if not request.form.get('password'):
            return render_template('login.html', error='Please enter a password')
        
        hash = execute_query('SELECT hash FROM users WHERE username = ?', username, one=True)['hash']
        if check_password_hash(hash, request.form.get('password')):
            # Add user's id to session
            session['user_id'] = execute_query('SELECT id FROM users WHERE username = ?', username, one=True)['id']
            return redirect('/')
        else:
            return render_template('login.html', error='Username or password is incorrect')
    else:
        return render_template('login.html')
    

@app.route('/register', methods = ['GET', 'POST'])
def register():
    ''' Register user by adding to database '''

    if request.method == 'POST':
        # Check username
        username = request.form.get('username')
        if not username:
            return render_template('register.html', error='Please enter a username')
        if execute_query('SELECT id FROM users WHERE username = ?', username, one=True):
            return render_template('register.html', error='User already exists')
        # Regular expression to check if the username starts with a letter and only contains letters and numbers
        if not match(r'^[A-Za-z][A-Za-z0-9]*$', username):
            return render_template('register.html', 
                                   error='Username must start with a letter and contain only letters and numbers')        

        # Check password
        if not request.form.get('password'):
            return render_template('register.html', error='Please enter a password')
        if request.form.get('password') != request.form.get('repeat_password'):
            return render_template('register.html', error='Passwords do not match')
        
        # Generate hash for password
        hash = generate_password_hash(request.form.get('password'))
        # Add user to database
        execute_query('INSERT INTO users (username, hash) VALUES (?, ?)', username, hash)
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/receive', methods=['POST'])
def receive():
    """
    Handle a POST request to receive a message and generate a response.

    This function receives a JSON with a 'recipient_id' key. It processes
    the message and generates a response, which is then returned as a JSON.
    The response is a list of dictionaries containing 'username', 'content',
    'timestamp', and 'id' (of messages) as keys. The function retrieves messages from the 
    database that are addressed to the recipient and orders them by timestamp
    in ascending order.
    
    Returns:
        A JSON response with a list of dictionaries containing the
        generated response.
    """

    recipient_id = request.json['recipient_id']

    # Check which messages to load
    old = request.json.get('old', False)

    if old:
        # Get last message id
        last_message_id = request.json.get('last_message_id', None)
        if last_message_id is None:
            last_message_id = execute_query('''
                                SELECT MAX(id) FROM messages 
                                WHERE (sender_id = ? AND recipient_id = ?) OR (sender_id = ? AND recipient_id = ?)
                                ''', recipient_id, session['user_id'], session['user_id'], recipient_id, one=True)
            last_message_id = last_message_id['MAX(id)'] if last_message_id['MAX(id)'] else -1
            last_message_id += 1
        # If load old messages
        response = execute_query('''
                    SELECT users.username, messages.content, messages.timestamp, messages.id FROM messages
                    JOIN users ON sender_id = users.id
                    WHERE ((sender_id = ? AND recipient_id = ?) OR (sender_id = ? AND recipient_id = ?))
                           AND messages.id < ?
                    ORDER BY messages.id DESC
                    LIMIT 30
                    ''', recipient_id, session['user_id'], session['user_id'], recipient_id, last_message_id)
    else:
        # If load new messages
        response = execute_query(''' 
                    SELECT users.username, messages.content, messages.timestamp, messages.id FROM messages
                    JOIN users ON sender_id = users.id
                    WHERE seen = 0 AND (sender_id = ? AND recipient_id = ?)
                    ORDER BY messages.id DESC
                    ''', recipient_id, session['user_id'])
        
    # Convert Row objects to dictionaries
    response = [dict(row) for row in response] if response else []

    # Get id of first and last message
    if response:
        first_id = response[-1]['id']
        last_id = response[0]['id']
    else:
        first_id = -1
        last_id = -1

    # Update seen status of messages in database
    execute_query('UPDATE messages SET seen = 1 WHERE (id >= ? AND id <= ?) AND recipient_id = ? AND seen = 0',
                first_id, last_id, session['user_id'])

    # Return a JSON response with the generated response
    return response



@app.route('/send', methods=['POST'])
def send():
    """
    Send a message.

    This function handles the POST request to send a message. It expects a
    JSON with a 'message' key. The message is stored in the database
    along with the sender's ID, a placeholder recipient ID, and the current
    timestamp.

    Returns:
        A JSON response with a 'status' key containing the string 'success'.
    """
    # Extract the message from the JSON
    message = request.json['message']
    recipient_id = request.json['recipient_id']

    # Store the message in the database
    execute_query('''
        INSERT INTO messages (sender_id, recipient_id, content, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', session['user_id'], recipient_id, message)

    # Return a JSON response indicating success
    return jsonify({'status': 'success'})


# Close connection to database at the end of request
app.teardown_appcontext(close_connection)
