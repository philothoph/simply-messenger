from flask import Flask, render_template, redirect, request

# Configure application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/chat', methods = ['GET', 'POST'])
def chat():
    return render_template('chat.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('login.html')