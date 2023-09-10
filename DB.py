import sqlite3

# Create or connect to the database file
conn = sqlite3.connect("game_identify.db")
cursor = conn.cursor()

# Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL
                 )''')

# Dashboard table
cursor.execute('''CREATE TABLE IF NOT EXISTS game_scores (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 score INTEGER,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (user_id) REFERENCES users(id)
                 )''')


conn.commit()
conn.close()