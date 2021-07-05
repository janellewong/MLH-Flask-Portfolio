import os
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"



@app.route('/')
def index():
    return render_template('main.html', title="Janelle Wong | Portfolio", url=os.getenv("URL"))

@app.route('/health', methods=['GET'])
def health():
	return "200"


@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password,
    password):
            error = 'Incorrect password.'

        if error is not None:
            return render_template('login.html', url=os.getenv("URL"), 
                message=error), 418

        if error is None:
            return render_template('login.html', url=os.getenv("URL"), 
                message="Login successful."), 200 
        else:
            return render_template('login.html', url=os.getenv("URL"), 
                message=error), 418
        

    return render_template('login.html',url=os.getenv("URL"))



@app.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        message = error
        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            message = f"User {username} created successfully"
            return render_template('register.html', url=os.getenv("URL"), 
                message=message), 200
        else:
            return error, 418


    return render_template('register.html',url=os.getenv("URL"))
    
