import sqlite3

def create_tables():
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


def register_user(username, email):
    conn = sqlite3.connect("game_identify.db")
    cursor = conn.cursor()

    try:
        # Attempt to insert a new user into the 'users' table
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        user_id = cursor.lastrowid  # Get the ID of the newly inserted user
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        # Handle the case where a user with the same username or email already exists
        conn.close()
        return None

def record_game_score(user_id, score):
    conn = sqlite3.connect("game_identify.db")
    cursor = conn.cursor()

    # Insert the game score into the 'game_scores' table
    cursor.execute("INSERT INTO game_scores (user_id, score) VALUES (?, ?)", (user_id, score))
    conn.commit()
    conn.close()

def get_leaderboard_entries():
    conn = sqlite3.connect("game_identify.db")
    cursor = conn.cursor()

    # Fetch the top 10 leaderboard entries ordered by time taken (assuming you have a 'game_scores' table)
    cursor.execute('''SELECT u.username, gs.score, gs.timestamp
                      FROM users AS u
                      INNER JOIN game_scores AS gs ON u.id = gs.user_id
                      ORDER BY gs.score DESC, gs.timestamp ASC
                      LIMIT 10''')

    leaderboard_data = cursor.fetchall()
    
    conn.close()
    return leaderboard_data




create_tables()

