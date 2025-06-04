import sqlite3
	
# Connect to database (creates books.db if it doesn't exist)
conn = sqlite3.connect('habits.db')
cursor = conn.cursor()
	
# Create table
cursor.execute('''
	CREATE TABLE IF NOT EXISTS habits (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    name TEXT NOT NULL,
	    date TEXT NOT NULL,
	    status TEXT CHECK(status IN ('done', 'missed')) NOT NULL,
        note TEXT
	)
	''')
	
conn.commit()
conn.close()
	
print("Database initialized.")