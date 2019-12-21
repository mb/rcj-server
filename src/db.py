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

	def create_database(self, schema_file):
		c = self.db.cursor()
		with open(schema_file) as f:
			c.executescript(f.read())
		self.db.commit()
	
	def store_run(self, competition, team_name, round, arena, referee, time_duration, start_time, end_time, scoring, comments, complaints, confirmed):
		"""
		Stores run in database overwrites existing runs from the same team on the same round
		arguments:
			* competition: string, should be unique for each compition
			* teamname: string, containing only ascii chars identifying the team
			* round: integer, together with competition and teamname the primary key
			* arena: id, identifying the arena
		"""
		c = self.db.cursor()
		c.execute('''INSERT INTO Run (competition, teamname, round, arena, referee, time_duration, timestamp_start, timestamp_end, scoring, comments, complaints, confirmed)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		''', (competition, team_name, round, arena, referee, time_duration, start_time, end_time, scoring, comments, complaints, confirmed))
	
	def get_runs(self, team_name):
		pass

	def get_runs_arena(self, team_name, arena):
		pass
	
	def get_runs_round(self, team_name, round):
		pass
	
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
		c.execute('''INSERT INTO referee (username, pwhash)
			VALUES (?, ?)
			ON CONFLICT(username)
			DO UPDATE SET pwhash=excluded.pwhash;
		''', (username, pwhash))
		self.db.commit()

