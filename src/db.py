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

	def create_database(self):
		c = self.db.cursor()
		c.execute("PRAGMA encoding = 'UTF-8';" )

		'''c.execute("""CREATE TABLE IF NOT EXISTS Referee(
			username	VARCHAR(64)   PRIMARY KEY,
			password	TEXT,
		)""")'''
		c.execute("""CREATE TABLE IF NOT EXISTS Referee(
			username VARCHAR(64) PRIMARY KEY,
			password TEXT
		);""")

		c.execute("""CREATE TABLE IF NOT EXISTS Run(
			competition TEXT,
			teamname TEXT,
			round INTEGER,
			arena TEXT,
			time_duration REAL,
			timestamp_start INTEGER,
			timestamp_end INTEGER,
			scoring TEXT,
			PRIMARY KEY(competition, teamname, round)
		);""")
		self.db.commit()
	
	def store_run(self, competition, team_name, round, arena, start_time, run_length, scoring, comments, complaints, confirmed):
		"""
		Stores run in database overwrites existing runs from the same team on the same round
		arguments:
			* competition: string, should be unique for each compition
			* teamname: string, containing only ascii chars identifying the team
			* round: integer, together with competition and teamname the primary key
			* arena: id, identifying the arena
		"""
		pass
	
	def get_runs(self, team_name):
		pass

	def get_runs_arena(self, team_name, arena):
		pass
	
	def get_runs_round(self, team_name, round):
		pass
	
	def get_referees(self):
		return self._query('SELECT * FROM referees')
	
	def get_referee_pwhash(self, username):
		return self._query('SELECT pwhash FROM referees WHERE username = ?', [username], one=True)
	
	def update_referee(self, username, pwhash):
		"""
		update or insert referee
		"""
		c = self.db.cursor()
		#https://stackoverflow.com/questions/15277373/
		c.execute('''INSERT INTO referees (username, pwhash)
			VALUES (?, ?)
			ON CONFLICT(username)
			DO UPDATE SET pwhash=excluded.pwhash;
		''')
		self.db.commit()

