from flask import Flask, render_template, redirect, request
from helpers import login_required

# Configure application
app = Flask(__name__)

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
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('login.html')
    

@app.route('/register')
def register():
    return render_template('register.html')
