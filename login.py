from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ketan@2005",
    database="Finzz"
)

# Cursor to execute queries
cursor = db.cursor()

# Index route to serve the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route to serve the signup form
@app.route('/signup', methods=['GET'])
def serve_signup_form():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match. Please try again."

        # Insert data into the database
        try:
            sql = "INSERT INTO users (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
            val = (username, firstname, lastname, email, password)
            cursor.execute(sql, val)
            db.commit()
            return redirect('login.html')  # Redirect to login page upon successful signup
        except mysql.connector.Error as err:
            return f"Error: {err}"  # Handle any database errors

if __name__ == '__main__':
    app.run(debug=True)
