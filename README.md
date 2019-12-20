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
pip install Flask flask-login
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
