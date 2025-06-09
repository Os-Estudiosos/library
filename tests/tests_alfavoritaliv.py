import unittest
from database import Connection
from database.tables.alfavoritaliv import AlFavoritaLivTable

class TestAlFavoritaLivTable(unittest.TestCase):
    def setUp(self):
        self.db_name = "livraria"
        self.path = "livraria"
        self.user = "joao.pedro"
        self.host = "10.61.49.160"
        self.password = "joao.pedro"
        self.conn = Connection(self.db_name, self.path, self.user, self.host, self.password)
        self.connection = self.conn.initialize()
        if self.connection:
            self.cursor = self.connection.cursor()
            self.connection.commit()
        self.table = AlFavoritaLivTable(self.connection)

    def tearDown(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def test_create(self):
        isbn = "9781686923500"
        matricula = "071"
        self.table.create(isbn, matricula)
        self.cursor.execute("SELECT MatriculaAl FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], matricula, "Falha ao criar registro na tabela AlFavoritaLiv")
        self.cursor.execute("DELETE FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        self.connection.commit()

    def test_read(self):
        isbn = "9781686923500"
        matricula = "071"
        self.cursor.execute("INSERT INTO AlFavoritaLiv (ISBNLiv, MatriculaAl) VALUES (%s, %s)", (isbn, matricula))
        self.connection.commit()
        result = self.table.read(qtd=1)
        self.assertIn("registros", result, "Falha ao ler registros da tabela AlFavoritaLiv")
        self.assertGreater(len(result["registros"]), 0, "Nenhum registro retornado")
        self.cursor.execute("DELETE FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        self.connection.commit()

    def test_update(self):
        isbn = "9781686923500"
        matricula_antiga = "071"
        matricula_nova = "67890"
        self.cursor.execute("INSERT INTO AlFavoritaLiv (ISBNLiv, MatriculaAl) VALUES (%s, %s)", (isbn, matricula_antiga))
        self.connection.commit()
        self.table.update(isbn, matricula_nova)
        self.cursor.execute("SELECT MatriculaAl FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], matricula_nova, "Falha ao atualizar registro na tabela AlFavoritaLiv")
        self.cursor.execute("DELETE FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        self.connection.commit()

    def test_delete(self):
        isbn = "9781686923500"
        matricula = "071"
        self.cursor.execute("INSERT INTO AlFavoritaLiv (ISBNLiv, MatriculaAl) VALUES (%s, %s)", (isbn, matricula))
        self.connection.commit()
        self.table.delete(isbn, matricula)
        self.cursor.execute("SELECT COUNT(*) FROM AlFavoritaLiv WHERE ISBNLiv = %s", (isbn,))
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 0, "Falha ao excluir registro da tabela AlFavoritaLiv")

if __name__ == '__main__':
    unittest.main(verbosity=2)