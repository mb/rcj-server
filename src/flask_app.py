
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello from Flask!'

@app.route('/api/submit_run', methods=['PUT', 'POST'])
def submit_run():
    if request.is_json:
        return "json"
    else:
        return "Not json"

