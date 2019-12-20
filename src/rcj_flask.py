from flask import Flask, request
from flask import g # global variables
from rcj import Rcj
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

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
	pwhash = g.rcj.get_referee_pwhash(username)
	if pwhash == None:
		return
	return check_password_hash(pwhash, password)

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
def submit_run():
	if request.is_json:
		return "json"
	else:
		return "Not json"

