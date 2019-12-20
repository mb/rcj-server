import sqlite3

class RcjDb:
    def __init__(self, database):
        # database: name of sqlite3 file
        self.db = database

    def create_database(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("'PRAGMA encoding = 'UTF-8';" )

        c.execute("""CREATE TABLE Referee(
            username    VARCHAR(64)   PRIMARY KEY,
            salt        VARCHAR
            FOREIGN KEY(competition) REFERENCES competition(name)
        )""")

        c.execute("""CREATE TABLE Run(
            competition TEXT,
            teamname TEXT,
	    round INTEGER,
            FOREIGN KEY(arena_id) REFERENCES arena(id),
            PRIMARY KEY(competition)
        )""")


