from flask import Flask, jsonify, render_template, redirect, request, session
from flask_session import Session
from helpers import close_connection, execute_query, login_required
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
    contacts = execute_query('''
                             SELECT username FROM users WHERE id IN 
                             (SELECT recipient_id FROM messages WHERE sender_id = ?)
                             ''', session['user_id'])
    contacts = [contact['username'] for contact in contacts]
    return render_template('index.html', contacts=contacts)
    

@app.route('/chat')
@login_required
def chat():
    name = request.args.get('name')
    recipient_id = execute_query('SELECT id FROM users WHERE username = ?', request.args.get('name'), one=True)
    if recipient_id:
        recipient_id = recipient_id['id']
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
        # Check password
        hash = execute_query('SELECT hash FROM users WHERE username = ?', username, one=True)['hash']
        if check_password_hash(hash, request.form.get('password')):
            # Add user's id to session
            session['user_id'] = execute_query('SELECT id FROM users WHERE username = ?', username, one=True)['id']
        return redirect('/')
    else:
        return render_template('login.html')
    

@app.route('/register', methods = ['GET', 'POST'])
def register():
    ''' Register user by adding to database '''

    if request.method == 'POST':
        # Check username
        username = request.form.get('username')
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
    Receive a message and generate a response.

    This function handles a POST request to receive a message. It expects a
    JSON with a 'message' key. The function processes the message and generates
    a response, which is then returned as a JSON.

    Returns:
        A JSON response with a 'message' key containing the generated response.
    """

    recipient_id = request.json['recipient_id']

    # Process the message and generate a response
    response = execute_query(''' 
                    SELECT sender_id, content FROM messages 
                    WHERE (sender_id = ? AND recipient_id = ?) OR (sender_id = ? AND recipient_id = ?) 
                    ORDER BY timestamp ASC
                    ''', session['user_id'], recipient_id, recipient_id, session['user_id'])

    # Convert Row objects to dictionaries
    response = [dict(row) for row in response]

    # Return a JSON response with the generated response
    return response



@app.route('/send', methods=['POST'])
def send():
    """
    Send a message.

    This function handles the POST request to send a message. It expects a
    JSON with a 'message' key. The message is stored in the database
    along with the sender's ID, a placeholder recipient ID, and the current
    timestamp. Currently, the recipient ID is fixed to 0.

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
