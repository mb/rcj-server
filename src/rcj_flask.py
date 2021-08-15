from flask import Flask, request, Response, send_from_directory
from flask import g # global variables
from rcj import Rcj
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
import json
from flask_cors import CORS

from configparser import ConfigParser

# read config file
parser = ConfigParser()
parser.read("rcj_config.ini")

# setup flask
app = Flask(__name__, static_url_path='')
CORS(app,
    supports_credentials=True,
    resources={
        r'/api/*': {
            'origins': ['https://rcjberlin.github.io', 'https://nikolockenvitz.de']
        }
    })

import os

# init the login manager
auth = HTTPBasicAuth()

# send digital scoring sheet
@app.route('/dss/<path:path>')
def send_dss(path):
    return send_from_directory('../rcj-dss', path)

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

@app.route('/api/v1/cors_test')
def test():
    return 'ok'

@app.route('/api/v1/login_required')
@auth.login_required
def login_required():
    return 'ok'

@app.route('/api/v1/submit_run', methods=['PUT', 'POST'])
@auth.login_required
def submit_run():
    # check for valid json
    if not request.is_json:
        return 'not json', 400
    run = request.json

    # add username and self computed scoring to dictionary
    run['referee'] = auth.username()
    try:
        g.rcj.store_run(run)
    except ValueError as e:
        return "{}: {}".format('ValueError', str(e)), 400
    return 'ok', 200

@app.route('/api/v1/dump_runs', methods=['GET'])
@auth.login_required
def dump_runs():
    return jsonify({'runs': g.rcj.dump_runs()})

@app.route('/api/v1/get_runs', methods=['GET'])
@auth.login_required
def get_runs():
    return jsonify({'runs': g.rcj.get_runs()})

@app.route('/api/v1/get_runs/competition/<string:competition>', methods=['GET'])
@auth.login_required
def get_runs_competition(competition):
    return jsonify({'runs': g.rcj.get_runs_competition(competition)})

def api_v2_check_auth(request):
    if 'referee' in request:
        if 'name' in request['referee'] and 'auth' in request['referee']:
            username = request['referee']['name']
            password = request['referee']['auth']
            return g.rcj.check_referee_password(username, password)
    return False

@app.route('/crud', methods=['GET'])
def crud():
    return send_from_directory('../public', 'crud.html')
@app.route('/crud/main.js', methods=['GET'])
def crud_main_js():
    return send_from_directory('../public', 'main.js')

@app.route('/api/v2/sql', methods=['POST'])
def sql():
    if not request.is_json:
        return jsonify({'error': 'not json'}), 400
    req = request.json

    if not api_v2_check_auth(req):
        return jsonify({'error': 'Unauthorized'}), 401
    if req['referee']['name'] not in ["niko", "manuel"]:
        return jsonify({'error': 'Forbidden'}), 403

    sql_statement = req['sqlStatement']
    if sql_statement.strip().lower() == "schema":
        result = [{'statement': 'schema',
                    'result': [],
                    'description': []}]
        tables = g.rcj.db._query_db("select name, sql from sqlite_master where type = 'table';")
        for table in tables:
            # split sql-create-statement into lines
            temp = table['sql'].split("\n")
            # remove comments
            temp = [line.split("--")[0] for line in temp]
            # join back to one line
            temp = " ".join(temp)
            # remove beginning of statement
            temp = temp.split("CREATE TABLE "+table['name']+"(")[1].strip()
            # remove bracket content (especially the commas inside would cause trouble)
            op, temp2 = 0, ""
            for letter in temp:
                if (letter == "("): op += 1
                if (op == 0): temp2 += letter
                if (letter == ")"): op -= 1
            # split at commas
            temp = [el.strip() for el in temp2.split(",")]
            # remove other instructions from create-statement like keys and constraints
            sql_keywords = ["PRIMARY KEY", "FOREIGN KEY", "REFERENCES", "CONSTRAINT"]
            temp2 = []
            for el in temp:
                for sql_keyword in sql_keywords:
                    if el.lower().startswith(sql_keyword.lower()):
                        break
                else: # else of for gets executed when finished normally (w/o break)
                    temp2.append(el)
            # use only first word as column name and second word as type
            column_names_w_type = [" ".join(el.split()[:2]) for el in temp2]
            # add table name
            names = [table['name']] + column_names_w_type
            result[0]['result'].append(names)
            result[0]['description'] = [""]*max(len(result[0]['description']),len(names))
    else:
        result = g.rcj.execute_sql_statement(sql_statement)

    # logging?
    return jsonify(result)

@app.route('/schedule/runs', methods=['GET'])
def get_scheduled_runs():
    return send_from_directory('../schedule', 'scheduled-runs.json')
@app.route('/schedule/json/<string:filename>', methods=['GET'])
def get_schedule_json_file(filename):
    if (filename in ["teams.json", "events.json", "competitions.json", "arenas.json", "scheduled-runs.json"]):
        return send_from_directory('../schedule', filename)
    # TODO: maps need to be filtered based on runs/dates (so that nothing is revealed too early)
    return "Not Found", 404

@app.route('/schedule', methods=['GET'])
def schedule():
    return send_from_directory('../schedule', 'index.html')
@app.route('/schedule/main.js', methods=['GET'])
def schedule_main_js():
    return send_from_directory('../schedule', 'main.js')
