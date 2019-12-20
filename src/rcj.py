from db import RcjDb

class Rcj:
	def _connect_db(self):
		"""
		creates new database object
		"""
		return sqlite3.connect(self._database_name)
	
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
			self._db.close()
	
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
	
	def is_referee(self, username):
		return True

