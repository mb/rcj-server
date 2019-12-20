
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask import g # global variables
from rcj import Rcj

from configparser import ConfigParser

parser = ConfigParser()
parser.read("rcj_config.ini")

app = Flask(__name__)
app.secret_key = parser.get('flask', 'secret_key')

# https://flask-doc.readthedocs.io/en/latest/patterns/sqlite3.html
@app.before_request
def before_request():
	g.rcj = Rcj(parser.get('db', 'filename'))

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'rcj'):
        del g.rcj

@app.route('/')
def root():
	return 'Hello from Flask!'

@app.route('/api/submit_run', methods=['PUT', 'POST'])
def submit_run():
	if request.is_json:
		return "json"
	else:
		return "Not json"

