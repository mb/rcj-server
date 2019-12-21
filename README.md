# RCJ Server

## Setup

This project currently runs on [PythonAnywhere](https://pythonanywhere.com) with flask

### Flask

https://flask.palletsprojects.com/en/1.1.x/installation/

Setup

```bash
git clone https://github.com/mb/rcj-server
cd rcj-server
python3 -m venv venv
. venv/bin/activate
pip install Flask Flask-HTTPAuth
```

Running the development version:

```
FLASK_APP=src/rcj_flask.py flask run
```

## Configuring

Example `rcj_config.ini`

```ini
[db]
filename = "rcj_database.sqlite"

[flask]
secret_key = "`n!'XPma6m(X_xUZ:0,~qPsvj%;e'+_G"
```

## Run

[Auth with HTTP-Auth](https://de.wikipedia.org/wiki/HTTP-Authentifizierung#Basic_Authentication)

Generate authorization string for user `NL` with password `wbSwFU6tY1c`: `base64("NL:wbSwFU6tY1c") = Tkw6d2JTd0ZVNnRZMWM=`

Example http request:


```
POST /api/v1/submit_run HTTP/1.1
Authorization: Basic Tkw6d2JTd0ZVNnRZMWM=
Content-Type: application/json
Content-Length: ...

{
	"competition": "line",
	"arena": "A", 
	"round": "2", 
	"teamname": "pi++", 
	"time": {     
		"timeRun": 57.82108,
		"timestampRunStart": 1554854400,
		"timestampRunEnd": 1558665000
	},
	"scoring": {  
		"teamStarted": true
	},
	"comments": "",
	"confirmedByTeamCaptain": true,
	"complaints": ""
}
```
