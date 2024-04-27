from random import seed
import secrets
from flask import Flask, redirect, render_template, session, url_for, request
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send
# import socketio

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'finzz'

mysql = MySQL(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myfinzz/')
def myfinzz():
    return render_template('myfinzz/index.html')

@app.route('/myfinzz/expenses')
def expenses():
    return render_template('myfinzz/expenses.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            cur.close()
            if user:
                # Store user data in session
                session['user_id'] = user[0]
                session['username'] = user[1]
                # Redirect to the dashboard
                return redirect(url_for('dashboard'))
            else:
                # Authentication failed
                return redirect(url_for('index', error='Invalid username or password'))
        except mysql.connector.Error as err:
            # Handle database errors
            print("Error connecting to database:", err)
            return redirect(url_for('index', error='Database error'))


@app.route('/myfinzz/dashboard')
def dashboard():
    # Check if user is logged in (user data is stored in session)
    if 'user_id' in session:
        user_id = session['user_id']
        username = session['username']
        # You can fetch additional user data from the database here if needed
        return render_template('myfinzz/dashboard.html', username=username)
    else:
        # If user is not logged in, redirect to the login page
        return redirect(url_for('index'))

@socketio.on('connect')
def handle_connect():
    # Print a message to the server's console when a client connects
    print('Client connected successfully')

    # Send the greeting message when the client connects to the chat
    send('Hi, my name is Finzz and I am your budgeting AI assistant.', broadcast=False)


@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    send('Hi my name is Finzz. How can I help you?')

if __name__ == '__main__':
    # Use socketio.run() instead of app.run() to run the application with SocketIO support
    socketio.run(app, debug=True)
