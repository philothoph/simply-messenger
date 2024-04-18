from flask import Flask, jsonify, render_template, redirect, request, session
from flask_session import Session
from helpers import close_connection, execute, insert_user, login_required
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
    return render_template('index.html')
    

@app.route('/chat', methods = ['GET', 'POST'])
@login_required
def chat():
    request.args.get('id')
    return render_template('chat.html')


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
        hash = execute('SELECT hash FROM users WHERE username = ?', username, one=True)[0]
        if check_password_hash(hash, request.form.get('password')):
            # Add user's id to session
            session['user_id'] = execute('SELECT id FROM users WHERE username = ?', username, one=True)[0]
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
        insert_user(username, hash)
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/receive', methods=['POST'])
def receive():
    ''' Receive a message '''

    message = request.json['message']
    # Code to process message and generate response
    response = 'Placeholder response'
    return jsonify({'message': response})


@app.route('/send', methods=['POST'])
def send():
    ''' Send a message '''
    
    message = request.json['message']
    # Code to handle message send by the user (e.g. store it in database)
    # For now return a success message
    return jsonify({'status': 'success'})


# Close connection to database at the end of request
app.teardown_appcontext(close_connection)
