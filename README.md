# Simply Messenger

Simply Messenger is a simple, web-based messaging application built with the Python Flask framework. It offers a clean interface for users to send and receive messages in real time.

## Features

- User authentication system.
- Contact list with the ability to search for users.
- Real-time one-on-one chatting with other users.
- Notifications for new messages using tooltips.

## Installation

To set up Simply Messenger on your local machine, follow these steps:

1. Clone the repository:
    `git clone https://github.com/philothoph/simply-messenger.git`
2. Navigate into the project directory:
    `cd simply-messenger`
3. Install required dependencies:
    `pip install -r requirements.txt`
4. Run the Flask application:
    `flask run`

## Usage

After starting the app, navigate to `http://localhost:5000` in your web browser to access Simply Messenger.

- Register a new account or log in.
- Add contacts to your contact list.
- Click on a contact to start chatting.
- Type your message and hit send.

## Structure of the project

### Python Files

- `messenger.py`: The main Flask application file which contains the app configuration, route definitions, and view logic for user authentication, message sending, and chatting functionalities. At first it was named `app.py`, but it was easier to config nginx and gunicorn with another name and separate wsgi.py file.

- `helpers.py`: Includes helper functions to open and close database connections, execute SQL queries, and perform user authentication.

- `wsgi.py`: The entry point for WSGI-compatible servers like Gunicorn. It imports the app from `messenger.py` and allows it to be served by WSGI servers.

- `config.py`: Contains configuration variables for the application, such as the database file name.

### Templates

- `layout.html`: The layout template for the app, including the navigation bar and footer.

- `index.html`: The index template for the app, which displays the contact list and chat window.

- `chat.html`: The chat template for the app, which displays the chat window and message history.

- `login.html`: The login template for the app, which displays the login form.

- `register.html`: The registration template for the app, which displays the registration form.

### Static Files

- `styles.css`: The CSS stylesheet for the app. The most of the styling is done by Bootstrap but some of it is done by this CSS file.

- `messageScript.js`: JavaScript file that handles the sending and receiving of chat messages, manages the scrolling behavior in the chat box, and checks for new messages periodically.

- `tooltip.js`: JavaScript file that enables tooltips.

- `favicon.ico`: The icon for the app.

### Database

- `simply.db`: The SQLite database for the app. It stores user information, contact information, and chat messages.

### Other Files

- `requirements.txt`: The list of required Python packages for the app.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask for the web framework.
- Bootstrap for frontend styling.
- Codeium for javascript code linting and code formatting.
