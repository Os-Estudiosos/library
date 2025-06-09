import unittest
from database import Connection
from database.tables.livro import LivroTable
from datetime import date  

class TestLivroTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.livro_table = LivroTable(cls.connection)

    def test_create_livro(self):
        isbn_teste = "9780000000001"
        self.livro_table.create(isbn_teste, "Livro Teste", "Editora Teste", 1, "2023-01-01", 1)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", (isbn_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Livro Teste")
        self.assertEqual(result[1], "Editora Teste")
        self.assertEqual(result[2], 1)
        self.assertEqual(result[3], date(2023, 1, 1))  
        self.assertEqual(result[4], 1)
        self.livro_table.delete(isbn_teste)

    def test_create_livro_conflict(self):
        isbn_teste = "9780000000001"
        self.livro_table.create(isbn_teste, "Livro Teste", "Editora Teste", 1, "2023-01-01", 1)
        self.livro_table.create(isbn_teste, "Livro Atualizado", "Editora Atualizada", 2, "2024-01-01", 2)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", (isbn_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Livro Atualizado")
        self.assertEqual(result[1], "Editora Atualizada")
        self.assertEqual(result[2], 2)
        self.assertEqual(result[3], date(2024, 1, 1)) 
        self.assertEqual(result[4], 2)
        self.livro_table.delete(isbn_teste)

    def test_read_livros(self):
        result = self.livro_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), 2)
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)

    def test_read_livros_with_filter(self):
        isbn_existente = "9781686923500"
        result = self.livro_table.read(filter={"ISBNLiv": isbn_existente})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], isbn_existente)

    def test_update_livro(self):
        isbn_teste = "9780000000001"
        self.livro_table.create(isbn_teste, "Livro Teste", "Editora Teste", 1, "2023-01-01", 1)
        self.livro_table.update(isbn_teste, "Livro Atualizado", "Editora Atualizada", 2, "2024-01-01", 2)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", (isbn_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Livro Atualizado")
        self.assertEqual(result[1], "Editora Atualizada")
        self.assertEqual(result[2], 2)
        self.assertEqual(result[3], date(2024, 1, 1))  
        self.assertEqual(result[4], 2)
        self.livro_table.delete(isbn_teste)

    def test_update_livro_inexistente(self):
        isbn_inexistente = "9789999999999"
        self.livro_table.update(isbn_inexistente, "Livro Inexistente", "Editora Inexistente", 1, "2023-01-01", 1)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT * FROM Livro WHERE ISBNLiv = %s;", (isbn_inexistente,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_livro(self):
        isbn_teste = "9780000000001"
        self.livro_table.create(isbn_teste, "Livro Teste", "Editora Teste", 1, "2023-01-01", 1)
        self.livro_table.delete(isbn_teste)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT * FROM Livro WHERE ISBNLiv = %s;", (isbn_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_livro_inexistente(self):
        isbn_inexistente = "9789999999999"
        self.livro_table.delete(isbn_inexistente)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.livro_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)