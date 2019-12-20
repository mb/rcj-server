from db import RcjDb

class Rcj:
	def __init__(self):
		pass

	def store_run(self, competition, team_name, round, arena, start_time, run_length, scoring, comments, complaints, confirmed, log):
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

