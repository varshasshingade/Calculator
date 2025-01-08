from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock user data for demonstration purposes
users = {
    "user1": "password1",
    "user2": "password2"
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('select_operation'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('select_operation'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/select_operation', methods=['GET', 'POST'])
def select_operation():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        operation = request.form['operation']
        session['operation'] = operation
        return redirect(url_for('solve_problem'))

    return render_template('select_operation.html')

@app.route('/solve_problem', methods=['GET', 'POST'])
def solve_problem():
    if 'username' not in session:
        return redirect(url_for('login'))

    operation = session.get('operation')
    result = None

    if request.method == 'POST':
        number1 = session.get('number1', random.randint(1, 100))
        number2 = session.get('number2', random.randint(1, 100))
        session['number1'] = number1
        session['number2'] = number2

        correct_answer = None
        if operation == 'add':
            correct_answer = number1 + number2
        elif operation == 'subtract':
            correct_answer = number1 - number2
        elif operation == 'multiply':
            correct_answer = number1 * number2
        elif operation == 'divide':
            correct_answer = number1 / number2 if number2 != 0 else None

        user_answer = request.form.get('answer')
        if user_answer is not None:
            try:
                user_answer = float(user_answer)
                result = "Correct" if user_answer == correct_answer else "Wrong"
            except ValueError:
                result = "Invalid input"

        session.pop('number1', None)
        session.pop('number2', None)

    number1 = random.randint(1, 100)
    number2 = random.randint(1, 100)
    session['number1'] = number1
    session['number2'] = number2

    return render_template('solve_problem.html', number1=number1, number2=number2, operation=operation, result=result)

if __name__ == '__main__':
    app.run(debug=True)
