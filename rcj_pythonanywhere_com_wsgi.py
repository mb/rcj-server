# This file contains the WSGI configuration required to serve up your
# web application at http://rcj.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError

import time

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

def application(environ, start_response):
    host = environ.get('SERVER_NAME')
    path = environ.get('PATH_INFO')
    args = environ.get('QUERY_STRING')
    postargs = environ['wsgi.input'].read().decode()

    if path == '/' or True:
        status = '200 OK'
        content = "Hello, World!\n"
        f = open("testfile.txt","a")
        f.write(path + " " + args + "\n")
        f.close()
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content))), ('Access-Control-Allow-Origin', '*')]
    start_response(status, response_headers)
    yield content.encode('utf8')


# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set its path on the web app setup tab.
# Then come back here and import your application object as per the
# instructions below


# +++++++++++ CUSTOM WSGI +++++++++++
# If you have a WSGI file that you want to serve using PythonAnywhere, perhaps
# in your home directory under version control, then use something like this:
#
#import sys
#
#path = '/home/rcj/path/to/my/app
#if path not in sys.path:
#    sys.path.append(path)
#
#from my_wsgi_file import application  # noqa
