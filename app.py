from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from helpers import close_connection, insert_user, login_required
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
    return render_template('chat.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    ''' Log user in '''

    # Forget user_id
    session.clear()

    # If user reached route via sending username and password
    if request.method == 'POST':
        
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


# Close connection to database at the end of context
app.teardown_appcontext(close_connection)
