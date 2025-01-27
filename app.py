
#postgresql://trail_host_user:ED3g8DOGgiXXgoiyMIZIIJSF8fn5qI5N@dpg-cubr6sd6l47c73a46fk0-a.oregon-postgres.render.com/trail_host
#postgresql://trail_host_user:ED3g8DOGgiXXgoiyMIZIIJSF8fn5qI5N@dpg-cubr6sd6l47c73a46fk0-a/trail_host

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = '76y3fcklas12798hg783hbbifb5b89'


def get_db_connection():
    return psycopg2.connect(
        dbname="trail_host",
        user="trail_host_user",
        password="ED3g8DOGgiXXgoiyMIZIIJSF8fn5qI5N",
        host="dpg-cubr6sd6l47c73a46fk0-a.oregon-postgres.render.com",
        port="5432"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM UserCred WHERE EmailID = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result and result[2] == password:
            flash("Login successful!", "success")
            return render_template('blank.html')
        else:
            flash("Invalid username or password!", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # Handle form submission
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for('signup'))

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM UserCred WHERE EmailID = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            flash("Email already exists! Use another email", "error")
            cursor.close()
            connection.close()
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Passwords don't match. Please recheck.", "error")
            cursor.close()
            connection.close()
            return redirect(url_for('signup'))

        query = "INSERT INTO UserCred (EmailID, Password, ConfirmPassword) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, password, confirm_password))
        connection.commit()

        cursor.close()
        connection.close()

        flash("Signup successful", "success")
        return redirect(url_for('success'))

    # Render the signup form for GET requests
    return render_template('signup.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
