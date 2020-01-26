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
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

@app.route('/api/v1/submit_run', methods=['PUT', 'POST'])
@auth.login_required
def submit_run():
    resp = Response()
    # TODO: add cors to all responses
    resp.headers['Access-Control-Allow-Origin'] = 'https://rcjberlin.github.io'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    # check for valid json
    if not request.is_json:
        resp.status_code = 400
        resp.response = 'not json'
        return resp
    try:
        run = request.json
    except ValueError as e:
        resp.status_code = 400
        resp.response = str(e)

    # check for missing attributes
    attr = ['competition', 'teamname', 'round', 'arena', 'time_duration', 'time_start', 'time_end', 'scoring', 'comments', 'complaints', 'confirmed']
    missing = [el for el in attr if el not in run]
    # TODO: check types of attributes
    if missing != []:
        # TODO: write error in response text
        resp.status_code = 400
        resp.response = "Missing attributes: {}\n".format(", ".join(missing))
        return resp

    # add username and self computed scoring to dictionary
    run['referee'] = auth.username()
    run['score'] = 0 # TODO: calculate the score
    run['scoring'] = str(run['scoring']) # stringify the score for the database

    # log all valid incoming requests
    f = open("flast.log", "a")
    f.write(str(run) + "\n")
    f.close()
    g.rcj.store_run(run)
    return resp
