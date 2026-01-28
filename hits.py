import sqlite3
import pandas as pd

print("---- Bollywood Hit Movies ---- \n")

def create_and_populate_db(csv_file, db_file):
    try:
        # Read the CSV file, treating '\N' as NaN
        df = pd.read_csv(csv_file, na_values=['\\N'])
        
        # Remove duplicates based on imdb_id
        df.drop_duplicates(subset=['imdb_id'], keep='first', inplace=True)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {csv_file} is empty.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return

    conn = None
    try:
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Drop the table if it exists to ensure fresh start with correct schema
        cursor.execute('DROP TABLE IF EXISTS movies')

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
        df.to_sql('movies', conn, if_exists='append', index=False)

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during database operations: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
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
