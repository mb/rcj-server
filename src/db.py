import sqlite3

class RcjDb:
	def __init__(self, database):
		# database: name of sqlite3 file
		self.db = sqlite3.connect(self._database_name)

	def create_database(self):
		conn = sqlite3.connect(self.database)
		c = conn.cursor()
		c.execute("'PRAGMA encoding = 'UTF-8';" )

		c.execute("""CREATE TABLE Referee(
			username	VARCHAR(64)   PRIMARY KEY,
			salt		VARCHAR
			FOREIGN KEY(competition) REFERENCES competition(name)
		)""")

		c.execute("""CREATE TABLE Run(
			competition TEXT,
			teamname TEXT,
		round INTEGER,
		arena TEXT,

		time_duration FLOAT, --in seconds
		timestamp_start INTEGER, --unix timestamp
		timestamp_end INTEGER, --unix timestamp

		scoring TEXT,  -- json object

		PRIMARY KEY(competition, teamname, round),
		)""")


