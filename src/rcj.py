from db import RcjDb

class Rcj:
	def _connect_db(self):
		"""
		creates new database object
		"""
		return RcjDb(self._database_name)
	
	def _get_connection(self):
		"""
		connect to databe, if not already connected
		"""
		db = getattr(self, '_db', None)
		if db is None:
			db = self._db = self._connect_db()
		return db

	def __init__(self, database):
		self._database_name = database
	
	def __del__(self):
		if hasattr(self, '_db'):
			del self._db
	
	def create_database(self):
		db = self._get_connection()
		db.create_database()
	
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
	
	def get_referees(self, username):
		db = self._get_connection()
		return db.get_referees()
	
	def is_referee(self, username):
		return self.get_referee_pwhash(username) != None
	
	def get_referee_pwhash(self, username):
		db = self._get_connection()
		return db.get_referee_pwhash(username)
	
	def add_referee(self, username, password):
		# TODO: add explicit parameters
		pwhash = generate_password_hash(password)


