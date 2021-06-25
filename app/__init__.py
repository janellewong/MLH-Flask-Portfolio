import os
from . import db
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db
# import locale

# locale.setlocale(locale.LC_ALL,'en_US.UTF-8')

load_dotenv()
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)


@app.route('/')
def index():
    return render_template('main.html', title="Janelle Wong | Portfolio", url=os.getenv("URL"))

@app.route('/health')
def health():
    return render_template('health.html', title="Janelle Wong | health", url=os.getenv("URL"))

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    return render_template('register.html', title="Janelle Wong | register", url=os.getenv("URL"))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200 
        else:
            return error, 418
    
    return render_template('login.html', title="Janelle Wong | login", url=os.getenv("URL"))


