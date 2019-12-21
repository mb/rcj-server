from flask import Flask, request
from flask import g # global variables
from rcj import Rcj
from flask_httpauth import HTTPBasicAuth

from configparser import ConfigParser

# read config file
parser = ConfigParser()
parser.read("rcj_config.ini")

# setup flask
app = Flask(__name__)
app.secret_key = parser.get('flask', 'secret_key')

# init the login manager
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
	return g.rcj.check_referee_password(username, password)

@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'

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
@auth.login_required
def submit_run():
	if request.is_json:
		return "json"
	else:
		return "Not json"

