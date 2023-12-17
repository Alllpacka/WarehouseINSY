import sys

import psycopg2


class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """
        Connect to database and return connection
        """
        print("Connecting to PostgreSQL Database...")
        try:
            conn = psycopg2.connect(user="postgres", password="password", host="postgres", port="5432",
                                    database="postgres")
        except psycopg2.OperationalError as e:
            print(f"Could not connect to Database: {e}")
            sys.exit(1)

        return conn

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.conn.cursor()


db = Database()
