import unittest
import os
import sqlite3
import pandas as pd
from unittest.mock import patch, MagicMock
from io import StringIO
import hits

class TestHits(unittest.TestCase):

    def setUp(self):
        self.csv_file = 'test_data.csv'
        self.db_file = 'test_movies.db'
        # Create a sample CSV file
        data = {
            'imdb_id': ['tt1', 'tt2', 'tt1'], # Intentionally adding duplicate for test
            'title': ['Movie 1', 'Movie 2', 'Movie 1'],
            'original_title': ['Movie 1', 'Movie 2', 'Movie 1'],
            'is_adult': [0, 0, 0],
            'year_of_release': [2020, 2021, 2020],
            'runtime': [120, 130, 120],
            'genres': ['Drama', 'Action', 'Drama']
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_file, index=False)

    def tearDown(self):
        # Clean up files
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_positive_create_and_populate_db(self):
        """Test happy path: valid CSV to DB creation"""
        hits.create_and_populate_db(self.csv_file, self.db_file)
        
        self.assertTrue(os.path.exists(self.db_file))
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM movies")
        count = cursor.fetchone()[0]
        conn.close()
        
        # Should be 2 because of deduplication
        self.assertEqual(count, 2)

    def test_file_not_found(self):
        """Test executing with a non-existent CSV file"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            hits.create_and_populate_db('non_existent.csv', self.db_file)
            self.assertIn("Error: The file non_existent.csv was not found.", fake_out.getvalue())

    def test_empty_file_error(self):
        """Test executing with an empty CSV file"""
        empty_csv = 'empty.csv'
        with open(empty_csv, 'w') as f:
            pass
        
        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                hits.create_and_populate_db(empty_csv, self.db_file)
                self.assertIn(f"Error: The file {empty_csv} is empty.", fake_out.getvalue())
        finally:
            if os.path.exists(empty_csv):
                os.remove(empty_csv)

    def test_generic_exception_reading_csv(self):
        """Test generic exception handling during CSV read"""
        with patch('pandas.read_csv', side_effect=Exception("Boom!")):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                hits.create_and_populate_db(self.csv_file, self.db_file)
                self.assertIn("An unexpected error occurred while reading the CSV: Boom!", fake_out.getvalue())
                
    def test_sqlite_error(self):
        """Test sqlite3 error handling"""
        # Mock sqlite3.connect to return a mock connection that raises error on commit
        with patch('sqlite3.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.commit.side_effect = sqlite3.Error("DB Error")
            
            with patch('sys.stdout', new=StringIO()) as fake_out:
                hits.create_and_populate_db(self.csv_file, self.db_file)
                self.assertIn("A database error occurred: DB Error", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
