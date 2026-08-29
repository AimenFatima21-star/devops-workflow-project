import unittest
import sqlite3
from datetime import datetime

class TestApp(unittest.TestCase):
    def test_sqlite_connection(self):
        conn = sqlite3.connect(':memory:')
        self.assertIsNotNone(conn)
        conn.close()

    def test_pandas_import(self):
        import pandas as pd
        self.assertIsNotNone(pd)

if __name__ == '__main__':
    unittest.main()
