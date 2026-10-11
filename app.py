from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student-project-secret-key"


# Home Page
@app.route('/')
def home():
    if 'user_email' not in session:
        return redirect('/login')
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match."

        conn = sqlite3.connect("loan.db")
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already registered."

        # Insert new user
        hashed_password = generate_password_hash(password)

        cursor.execute("""
        INSERT INTO users(name,email,mobile,password)
        VALUES(?,?,?,?)
        """, (name, email, mobile, hashed_password))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("loan.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user:

            # user[4] = password column
            if check_password_hash(user[4], password):

                session['user_email'] = user[2]
                session['user_name'] = user[1]

                return redirect('/')

        return "Invalid Email or Password"

    return render_template("login.html")


# Loan Eligibility
@app.route('/check', methods=['POST'])
def check():

    if 'user_email' not in session:
        return redirect('/login')

    name = session['user_name']

    age = int(request.form['age'])
    income = float(request.form['income'])
    credit_score = int(request.form['credit_score'])
    loan_amount = float(request.form['loan_amount'])

    if age >= 21 and income >= 30000 and credit_score >= 700:
        result = "Loan Approved ✅"

    elif credit_score < 600:
        result = "Loan Rejected ❌ (Low Credit Score)"

    elif income < 30000:
        result = "Loan Rejected ❌ (Low Income)"

    else:
        result = "Further Verification Required"

    return render_template(
        "result.html",
        name=name,
        age=age,
        income=income,
        credit_score=credit_score,
        loan_amount=loan_amount,
        result=result
    )


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)