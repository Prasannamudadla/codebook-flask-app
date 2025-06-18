import sqlite3
import os

#Ensure the 'db' folder exists
os.makedirs('db',exist_ok = True)

#Connect to the database inside the 'db' folder
conn =  sqlite3.connect('db/codebook.db')
cursor = conn.cursor()  #creates a cursor object that allows us to execute SQL commands

cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        )
    ''')


#Insert sample questions
sample_data = [
    ("Two Sum","Arrays","Unsolved","Use hash map"),
    ("Merge Sort","Sorting","Solved","Divide and conquer"),
    ("Binary Search","searching","Unsolved","")
]

cursor.executemany('''
                   INSERT INTO questions(title,topic,status,notes)
                   vALUES(?,?,?,?)
                   ''',sample_data)

#save and close the connection
conn.commit()
conn.close()

print("Database initialized successfully in 'db/codebook.db'.")
