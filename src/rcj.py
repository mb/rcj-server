#!/usr/bin/env python3

from db import RcjDb
from werkzeug.security import generate_password_hash, check_password_hash
import json
import datetime

class Rcj:
    def __init__(self, database="rcj_database.sqlite"):
        self._database_name = database
        self.db = RcjDb(self._database_name)
    
    def __del__(self):
        if hasattr(self, '_db'):
            del self._db
    
    def create_database(self, schema_file):
        self.db.create_database(schema_file)

    def _log_run(self, run, comment):
        # use \t as separator, as json.dumps masks it with \\t
        line = "{date}\t{comment}\t{run}\n".format(
            date=datetime.datetime.utcnow().isoformat(),
            comment=comment,
            run=json.dumps(run)
        )
        with open('all_runs.log', 'a') as f:
            # TODO: check if this is a race bug
            f.write(line)
    
    def store_run(self, run):
        """
        raises ValueError on incorrect input data
        Stores run in database overwrites existing runs from the same team on the same round
        example dictionary for the parameter run:
            run = {
                'competition': 'line',
                'teamname': 'pi++',
                'round': '3',
                'arena': 'A',
                'referee': 'referee_run',
                'time_duration': 120.01,
                'time_start': 1576934336,
                'time_end': 1576934456,
                'scoring': '''{
                    teamStarted: true,
                    evacuationPoint: "high",
                    sections: [ ... ],
                    victims: {
                        deadVictimsBeforeAllLivingVictims: 3,
                        livingVictims: 2,
                        deadVictimsAfterAllLivingVictims: 0
                    },
                    leftEvacuationZone: false,
                    score: 314
                }'''.replace(' ', '').replace('\t', '').replace('\n', ''),
                'score': 314,
                'comments': 'comments from referees',
                'complaints': '',
                'confirmed': True,
            }
        If a value is missing from the dictionary, a ValueException is raised
        """
        # check for missing attributes and correct type
        attr = [
            ('competition', str),
            ('teamname', str),
            ('round', int),
            ('arena', str),
            ('time_duration', float),
            ('time_start', float),
            ('time_end', float),
            ('scoring', str),
            ('comments', str),
            ('complaints', str),
            ('confirmed', bool)
        ]
        missing = [el[0] for el in attr if el[0] not in run]
        if missing != []:
            raise ValueError("Missing attributes: {}\n".format(", ".join(missing)))
        wrong_type = ["{} (found {}, expected {})".format(el[0], type(run[el[0]]), el[1])
                for el in attr if type(run[el[0]]) != el[1]]
        if wrong_type != []:
            raise ValueError("Attributes with wrong type:\n{}".format("\n".join(wrong_type)))

        # TODO: calculate score and compare with previos result + result from rcj-dss
        # check if the run is already stored
        existing_run = self.db.get_run(run['competition'], run['teamname'], run['round'])
        if existing_run != None:
            self._log_run(run, "duplicate") # todo: check what is different
            raise ValueError("run already exists, but logged successfully")
 
        # log all valid incoming requests
        self._log_run(run, "ok")

        self.db.store_run(run)

    def get_runs(self):
        return self.db.get_runs()

    def get_runs_arena(self, arena):
        pass
    
    def get_runs_round(self, round):
        pass
    
    def get_referees(self):
        return self.db.get_referees()
    
    def is_referee(self, username):
        return self.db.get_referee_pwhash(username) != None
    
    def check_referee_password(self, username, password):
        pwhash = self.db.get_referee_pwhash(username)
        if pwhash == None:
            return False # user doen't exist
        return check_password_hash(pwhash, password)
    
    def update_referee(self, username, password):
        """
        adds referee overwrites if already exists
        """
        # TODO: add explicit parameters
        pwhash = generate_password_hash(password)
        self.db.update_referee(username, pwhash)

if __name__ == '__main__':
    import fire #cli
    fire.Fire(Rcj)
