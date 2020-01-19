from db import RcjDb
from werkzeug.security import generate_password_hash, check_password_hash

class Rcj:
    def __init__(self, database):
        self._database_name = database
        self.db = RcjDb(self._database_name)
    
    def __del__(self):
        if hasattr(self, '_db'):
            del self._db
    
    def create_database(self, schema_file):
        self.db.create_database(schema_file)
    
    def store_run(self, competition, teamname, round, arena, referee, time_duration, time_start, time_end, scoring, comments, complaints, confirmed):
        """
        Stores run in database overwrites existing runs from the same team on the same round
        arguments:
            * competition: string, should be unique for each compition
            * teamname: string, containing only ascii chars identifying the team
            * round: integer, together with competition and teamname the primary key
            * arena: id, identifying the arena
        """
        self.db.store_run(competition, teamname, round, arena, referee, time_duration, time_start, time_end, scoring, comments, complaints, confirmed)

    def get_runs(self, teamname):
        pass

    def get_runs_arena(self, teamname, arena):
        pass
    
    def get_runs_round(self, teamname, round):
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


