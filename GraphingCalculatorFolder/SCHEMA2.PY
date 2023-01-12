import sqlite3

conn = sqlite3.connect("GRAPHINGDATABASEFINAL.db")
cursor = conn.cursor()




cursor.execute("""CREATE TABLE IF NOT EXISTS UserTable
				(UserID integer PRIMARY KEY AUTOINCREMENT,
				FullName text,
				Username text,
				Password text)
				""")


cursor.execute("""CREATE TABLE IF NOT EXISTS EquationTable
				(ID integer PRIMARY KEY AUTOINCREMENT,
				UserID_1 integer,
				Username text,
				Equation text,
				Date Date,
				Time text,
				FOREIGN KEY (UserID_1) REFERENCES UserTable(UserID))
				""")





cursor.execute("""CREATE TABLE IF NOT EXISTS OccurancesTable
				(EquationOccuranceID integer PRIMARY KEY AUTOINCREMENT,
				UserID_2 integer,
				ID_2 integer,
				FOREIGN KEY(UserID_2) REFERENCES UserTable(UserID),
				FOREIGN KEY(ID_2) REFERENCES EquationTable(ID))
				""")

