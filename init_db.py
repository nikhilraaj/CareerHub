import sqlite3

DATABASE_FILE = "careerapp.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Create questions table
    cur.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        title TEXT NOT NULL,
        practice_link TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE
    )''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    create_tables()
