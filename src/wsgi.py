#!/usr/bin/env python

HTML_HEADER = """<!DOCTYPE html>
<html lang="de-DE">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RCJ 2020 Berlin - {title}</title>
</head>
<body>
<h1>{title}</h1>
"""
HTML_FOOTER = """</body>
</html>"""

import os
import sys

# https://palletsprojects.com/p/flask/

def application(environ, start_response):
    host = environ.get('SERVER_NAME')
    path = environ.get('PATH_INFO')
    args = environ.get('QUERY_STRING')
    postargs = environ['wsgi.input'].read().decode()
    status = ''
    content = ''

    if path == '/':
        status = '200 OK'
        content = "Hello, World!<br>\n"
        content += "Test page\n"
        f = open("testfile.txt","a")
        f.write(host + " " + path + " " + args + "\n")
        f.close()
    elif path == "/info":
        status = '200 OK'
        content = '<h1>Debug info</h1>\n'
        content += 'argv: ' + str(sys.argv) + '<br>\n'
        content += 'cwd: ' + os.getcwd() + '<br>\n'
    else:
        status = '404 NOT FOUND'
        content = path + 'Page not found.'

    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content))), ('Access-Control-Allow-Origin', '*')]
    start_response(status, response_headers)
    yield content.encode('utf8')



