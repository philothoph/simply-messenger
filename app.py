from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/login')
def login():
    return render_template('login.html')