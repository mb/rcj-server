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

    # redirect to HTTPS
    isHTTPS = environ.get('HTTPS')
    if(False):#isHTTPS == None or isHTTPS.lower() != 'on'):
        httpsURL = "https://" + str(host) + str(path)
        if(args != None and args != ""): httpsURL += '?'+str(args)

        status = '200 OK'
        content = '<html><header><meta http-equiv="refresh" content="0; url=' + httpsURL
        content+= '"/></header><body><p>Redirect to HTTPS</p><p><a href="' + httpsURL + '">' + httpsURL + '</a></p></body></html>'

        response_headers = [('Content-Type', 'text/html'),
                            ('Content-Length', str(len(content)))]

        start_response(status, response_headers)
        yield content.encode('utf8')

    if path == '/' or True:
        status = '200 OK'
        content = "Hello, World!"
        f = open("testfile.txt","a")
        f.write(path + " " + args + "\n")
        f.close()
    elif path == '/survey':
        status = '200 OK'
        content = HTML_HEADER.format(title="Test") + """
        <form action="/sendsurvey" method="post">
            <p>In welchem Wettbewerb wirst du teilnehmen?</p>
            <label><input type="radio" name="league" value="line"> Rescue Line</label> <br>
            <label><input type="radio" name="league" value="entry"> Rescue Line Entry</label>

            <p>Hast du bereits im letzten Jahr beim RCJ Qualifikationsturnier in Berlin teilgenommen?</p>
            <label><input type="radio" name="participation2019" value="yes" onchange="onchange2019()"> Ja</label> <br>
            <label><input type="radio" name="participation2019" value="no" onchange="onchange2019()"> Nein</label>

        <script>
        function onchange2019 () {
            let radios = document.getElementsByName('participation2019');
            for (var i=0; i<radios.length; i++) {
                if (radios[i].checked) {
                    document.getElementById("block-last-year").style.display = (radios[i].value == "yes") ? "" : "none";
                    break;
                }
            }
        }
        </script>

        <span id="block-last-year">
            <p>Wie zufrieden warst du im letzten Jahr (2019)?</p>
            <table border="1" cellspacing="0">
            <tr><td></td><td>--</td><td>-</td><td>0</td><td>+</td><td>++</td></tr>
            </table>
        </span>
            <!--Kommentar-->

            <p>Wenn du möchtest, kannst du noch ein paar weitere freiwillige Angaben machen.</p>
            <label for="teamname">Teamname: </label>
            <input type="text" name="teamname"> <br>

            <label for="age">Alter: </label>
            <input type="number" name="age" min="0" max="19" value="0"> <br>

            <label for="grade">Klassenstufe: </label>
            <input type="number" name="grade" min="1" max="13" value="1"> <br>


            <!-- Anzahl Teilnahmen, letztes Jahr Berlin?, Teamname, Alter, Klassenstufe, Region, Zeitaufwand, Regeln gelesen/vertraut - Englisch? kompliziert umfangreich
            Zufriedenheit 2019 (orga, schiris, live ergebnisse samstag)
            schwierigkeit der parcours insgesamt zu leicht / schwer; einzelne Platten leicht / schwer
            Reihenfolge Teams (Zufall, Schule am stück, möglichst weit auseinander)
            Anzahl Läufe
            Streichlauf
            Zeitplan (13-18Uhr)
            Ergebnisse bereits vor der Siegerehrung bekannt geben (live, wie samstag)
            Showläufe
            sonstige ideen anregung kritik
            -->

            <input type="submit" value="Umfrage abschicken!">
        </form>
        """ + HTML_FOOTER
    elif path == '/sendsurvey':
        status = '200 OK'
        content = HTML_HEADER.format(title="Danke!") + "<p>Vielen Dank für die Teilnahme an der Umfrage! Bis zum RoboCup im März!</p>" + HTML_FOOTER
        f = open("surveyresults.txt", "a")
        f.write(time.strftime("%Y-%m-%d %T") + " " + postargs + "\n")
        f.close()
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
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
