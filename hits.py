import sqlite3
import pandas as pd

print("---- Bollywood Hit Movies ---- \n")

def create_and_populate_db(csv_file, db_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        imdb_id TEXT PRIMARY KEY,
        title TEXT,
        original_title TEXT,
        is_adult INTEGER,
        year_of_release INTEGER,
        runtime INTEGER,
        genres TEXT
    )
    ''')

    # Insert data into the table
    df.to_sql('movies', conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

# Usage
csv_file = './bollywood_meta_2010-2019.csv'
db_file = './bollywood_movies.db'
create_and_populate_db(csv_file, db_file)

print("Database created and data inserted successfully.")

print("---- Printing hit Movies ---- \n")

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Query to select all rows from the movies table
cursor.execute('SELECT * FROM movies')

# Fetch all rows
rows = cursor.fetchall()

# Display the rows
for row in rows:
    print(row)

# Close the connection
conn.close()

print("---- Hit Movies Printed DONE  ---- \n")
