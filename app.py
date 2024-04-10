from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Through POST shows contacts list
    # Through GET - login page
    if request.method == 'POST':
        return render_template('contacts.html')
    else:
        return render_template('index.html')
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')