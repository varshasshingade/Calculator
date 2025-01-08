from flask import Flask, render_template, redirect,request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegistrationForm, LoginForm
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'b9f8eb5e3cd24a4e9dfe602a94f023bc'


db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('inlogin')
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('arithmetic'))
            flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)
    except Exception as e:
        print('exception', e)
        return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/arithmetic', methods=['GET', 'POST'])
@login_required
def arithmetic():
    if 'question' not in session:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        operation = random.choice(['+', '-', '*', '/'])
        question = f"{num1} {operation} {num2}"
        answer = eval(question) if operation != '/' else round(num1 / num2, 2)
        session['question'] = question
        session['answer'] = answer

    if request.method == 'POST':
        user_answer = float(request.form.get('answer'))
        correct = user_answer == session['answer']
        flash(f"{'Correct!' if correct else 'Wrong!'} The answer was {session['answer']}.", 'info')
        session.pop('question')
        session.pop('answer')
        return redirect(url_for('arithmetic'))

    return render_template('arithmetic.html', question=session['question'])




from flask import Flask, render_template, redirect, url_for
from forms import ArithmeticOperationForm

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/select_operation', methods=['GET', 'POST'])
def select_operation():
    form = ArithmeticOperationForm()
    if form.validate_on_submit():
        selected_operation = form.operation.data
        return redirect(url_for('perform_operation', operation=selected_operation))
    return render_template('select_operation.html', form=form)

@app.route('/perform_operation/<operation>', methods=['GET', 'POST'])
def perform_operation(operation):
    import random
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)

    if operation == 'add':
        result = num1 + num2
        operation_symbol = '+'
    elif operation == 'subtract':
        result = num1 - num2
        operation_symbol = '-'
    elif operation == 'multiply':
        result = num1 * num2
        operation_symbol = '*'
    elif operation == 'divide':
        result = num1 / num2 if num2 != 0 else 'Undefined (division by 0)'
        operation_symbol = '/'

    return render_template('perform_operation.html', num1=num1, num2=num2, operation_symbol=operation_symbol, result=result)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
