import sqlite3
import pandas as pd

# Read the CSV file
csv_file = '/Users/rhishijoshi/Hits/bollywood_meta_2010-2019.csv'
df = pd.read_csv(csv_file)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('/Users/rhishijoshi/Hits/bollywood_movies.db')
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

print("Database created and data inserted successfully.")

print("---- Hit Movies ---- \n")


print("---- Logic ---- \n")
print("---- Logic Line 2 ---- \n")
print("---- Logic Line 3 ---- \n")
print("---- ----\n")
