from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = '76y3fcklas12798hg783hbbifb5b89'

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "lasya@23#",
    database = "mywebsitedata"
)
mycursor = mydb.cursor()

def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS UserCred (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        EmailID VARCHAR(255) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        ConfirmPassword VARCHAR(255) NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    mycursor.execute(create_table_query)
    print("UserCred table created (if it didn't already exist).")

#create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM UserCred WHERE EmailID = %s"
        mycursor.execute(query, (username, ))
        result = mycursor.fetchone()

        if result and result[2] == password:
            flash("login successful!", "success")
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

        query = "SELECT * FROM UserCred WHERE EmailID = %s"
        mycursor.execute(query, (email,))
        result = mycursor.fetchone()

        if result:
            flash("Email already exists! Use another email", "error")
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Passwords don't match. Please recheck.", "error")
            return redirect(url_for('signup'))

        query = "INSERT INTO UserCred (EmailID, Password, ConfirmPassword) VALUES (%s, %s, %s)"
        mycursor.execute(query, (email, password, confirm_password))
        mydb.commit()

        flash("Signup successful", "success")
        return redirect(url_for('success'))

    # Render the signup form for GET requests
    return render_template('signup.html')


@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug = True)

