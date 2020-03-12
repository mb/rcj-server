import sqlite3

class RcjDb:
    def __init__(self, database):
        # database: name of sqlite3 file
        self.db = sqlite3.connect(database)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def _query_db(self, query, args=(), one=False):
        cur = self.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]

        if one:
            if rv:
                return rv[0]
            else:
                return None
        else:
            return rv

    def _execute_statement(self, statement):
        # split into multiple statements in case there are multiple
        statements = [s.strip() for s in statement.replace("\n", " ").split(";")]
        r = []
        for statement in statements:
            if(statement == ""): continue
            try:
                cur = self.db.execute(statement)
                r.append({'statement': statement,
                            'result': cur.fetchall(),
                            'description': [el[0] for el in cur.description] if cur.description else []})
            except Exception as e:
                return {'error': str(e), 'statement': statement}
        self.db.commit()
        return r

    def create_database(self, schema_file):
        c = self.db.cursor()
        with open(schema_file) as f:
            c.executescript(f.read())
        self.db.commit()

    def get_run(self, competition, teamname, round):
        return self._query_db("SELECT * FROM Run WHERE competition=? AND teamname=? AND round=?", (competition, teamname, round), one=True)
    
    def store_run(self, run):
        """
        Stores run in database overwrites existing runs from the same team on the same round
        arguments:
            * competition: string, should be unique for each compition
            * teamname: string, containing only ascii chars identifying the team
            * round: integer, together with competition and teamname the primary key
            * arena: id, identifying the arena
        """
        c = self.db.cursor()
        c.execute('''INSERT INTO Run (competition, teamname, round, arena, referee, time_duration, time_start, time_end, scoring, score, comments, complaints, confirmed)
            VALUES (:competition, :teamname, :round, :arena, :referee, :time_duration, :time_start, :time_end, :scoring, :score, :comments, :complaints, :confirmed)''',
            run)
        self.db.commit()
    
    def dump_runs(self):
        return self._query_db("SELECT * FROM Run")

    def get_runs(self):
        return self._query_db("SELECT competition, teamname, round, arena, time_duration, score FROM Run")

    def get_runs_competition(self, competition):
        return self._query_db("SELECT teamname, round, arena, time_duration, score FROM Run WHERE competition=?", (competition,))
    
    def get_referees(self):
        return self._query_db('SELECT * FROM referee')
    
    def get_referee_pwhash(self, username):
        pwhash = self._query_db('SELECT pwhash FROM referee WHERE username = ?', [username], one=True)
        # unwrap the resulting dictionary into the password hash string
        if pwhash == None:
            return
        return pwhash['pwhash']
    
    def update_referee(self, username, pwhash):
        """
        update or insert referee
        """
        c = self.db.cursor()
        #https://stackoverflow.com/questions/15277373/
        c.execute('''INSERT OR REPLACE INTO referee (username, pwhash) VALUES (?, ?)''', (username, pwhash))
        self.db.commit()

