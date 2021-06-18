import os
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
# import locale

# locale.setlocale(locale.LC_ALL,'en_US.UTF-8')


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Bob Zoldyck | Portfolio", url=os.getenv("URL"))




