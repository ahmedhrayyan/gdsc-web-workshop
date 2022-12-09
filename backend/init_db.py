import sqlite3

db = sqlite3.connect("tutorial.db")

db.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, date DATETIME, is_done INTEGER DEFAULT 0)")
