from flask import Flask, request, Response, send_from_directory
from flask import g # global variables
from rcj import Rcj
from flask_httpauth import HTTPBasicAuth

from configparser import ConfigParser

# read config file
parser = ConfigParser()
parser.read("rcj_config.ini")

# setup flask
app = Flask(__name__, static_url_path='')

import os

# init the login manager
auth = HTTPBasicAuth()

@app.route('/dss/<path:path>')
def send_dss(path):
	#return path
	return send_from_directory('../rcj-dss', path)
	#return os.getcwd()
	#return send_from_directory('../', 'db.py')


@auth.verify_password
def verify_password(username, password):
	return g.rcj.check_referee_password(username, password)

# https://flask-doc.readthedocs.io/en/latest/patterns/sqlite3.html
@app.before_request
def before_request():
	g.rcj = Rcj(parser.get('db', 'filename'))

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'rcj'):
		del g.rcj

@app.route('/')
@auth.login_required
def root():
	return 'Hello from Flask!'

@app.route('/test')
def test():
	resp = Response()
	resp.headers['Access-Control-Allow-Origin'] = 'https://nikolockenvitz.de'
	resp.headers['Access-Control-Allow-Credentials'] = 'true'
	return resp

@app.route('/api/v1/submit_run', methods=['OPTIONS'])
@auth.login_required
def submit_run_cors():
	resp = Response()
	resp.headers['Access-Control-Allow-Origin'] = 'https://nikolockenvitz.de'
	resp.headers['Access-Control-Allow-Credentials'] = 'true'
	resp.headers['Access-Control-Allow-Methods'] = 'POST'
	return resp

@app.route('/api/v1/submit_run', methods=['PUT', 'POST'])
@auth.login_required
def submit_run():
	resp = Response()
	resp.headers['Access-Control-Allow-Origin'] = 'https://nikolockenvitz.de'
	resp.headers['Access-Control-Allow-Credentials'] = 'true'
	if request.is_json:
		f = open("log", "a")
		f.write(str(request.json) + "\n")
		f.close()
		j = request.json
		competition = j['competition']
		teamname = j['teamname']
		round = j['round']
		arena = j['arena']
		referee = auth.username()
		time_duration = j['time']['timeRun']
		time_start = j['time']['timestampRunStart']
		time_end = j['time']['timestampRunEnd']
		scoring = str(j['scoring'])
		comments = j['comments']
		complaints = j['complaints']
		confirmed = j['confirmedByTeamCaptain']
		g.rcj.store_run(competition, teamname, round, arena, referee, time_duration, time_start, time_end, scoring, comments, complaints, confirmed)
		resp.status_code = 200
		resp.status = 'OK'
	else:
		resp.status_code = 400
		resp.status = 'NOT JSON'
	return resp


