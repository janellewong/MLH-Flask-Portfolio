import os
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
from flask import Flask, request, render_template
# import locale

# locale.setlocale(locale.LC_ALL,'en_US.UTF-8')

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Bob Zoldyck | Portfolio", url=os.getenv("URL"))

@app.route('/health')
def health():
    return render_template('health.html', title="Bob Zoldyck | Portfolio", url=os.getenv("URL"))




