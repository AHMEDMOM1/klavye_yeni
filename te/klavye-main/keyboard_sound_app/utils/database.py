import sqlite3

class Database:
    def __init__(self, db_name="keyboard_sound.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def execute(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_one(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetch_all(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.close()