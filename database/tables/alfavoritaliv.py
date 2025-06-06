import psycopg2
from database import Connection
from database.tables import Table

class Alfavoritaliv(Connection.initialize):
    def __init__(self, db_name, path, owner):
        super().__init__(db_name, path, owner)
        self.conn = self.initialize()
        