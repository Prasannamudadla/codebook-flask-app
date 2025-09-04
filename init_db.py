import sqlite3
import os

# Ensure the 'db' folder exists
os.makedirs('db', exist_ok=True)

# Connect to the database
conn = sqlite3.connect('db/codebook.db')
cursor = conn.cursor()

# Drop table if exists (so we start fresh)
cursor.execute("DROP TABLE IF EXISTS questions")

# Create table with user_id
cursor.execute('''
    CREATE TABLE questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        user_id INTEGER
    )
''')

# Insert sample questions with user_id = 1 (or any test user)
sample_data = [
    ("Two Sum", "Arrays", "Unsolved", "Use hash map", 1),
    ("Merge Sort", "Sorting", "Solved", "Divide and conquer", 1),
    ("Binary Search", "Searching", "Unsolved", "", 1)
]

cursor.executemany('''
    INSERT INTO questions(title, topic, status, notes, user_id)
    VALUES (?, ?, ?, ?, ?)
''', sample_data)

# Save and close
conn.commit()
conn.close()

print("Database initialized successfully in 'db/codebook.db'.")
