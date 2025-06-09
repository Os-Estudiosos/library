from database import Connection
import unittest

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.db_name = "livraria"
        self.path = "livraria"
        self.user = "thalis"
        self.host = "10.61.49.160"
        self.password = "thalis"  
        self.conn = Connection(self.db_name, self.path, self.user, self.host, self.password)

    def test_connection_initialization(self):
        connection = self.conn.initialize()
        self.assertIsNotNone(connection, "Falha ao conectar ao banco de dados")
        if connection:
            connection.close()

    def test_string_representation(self):
        expected_output = f"O banco de dados {self.db_name} está sendo usado por {self.user} e tem o caminho {self.path}"
        result = str(self.conn)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()