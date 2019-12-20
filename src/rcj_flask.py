from flask import Flask, request
from flask import g # global variables
from rcj import Rcj
import flask_login

from configparser import ConfigParser

# read config file
parser = ConfigParser()
parser.read("rcj_config.ini")

# setup flask
app = Flask(__name__)
app.secret_key = parser.get('flask', 'secret_key')

# init the login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# user class for the login manager
class Referee(flask_login.UserMixin):
	pass

# called when checking if a user exists
@login_manager.user_loader
def load_user(user_id):
	if not g.rcj.is_referee(user_id):
		return
	user = Referee()
	user.id = user_id
	return user

@login_manager.request_loader
def request_loader(request):
	username = request.form.get("username")
	# timing attack :/
	if not g.rcj.is_referee(user_id):
		return
	user = Referee()
	user.id = username
	password = request.form.get("password")

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return 'Logged out'

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

