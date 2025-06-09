import unittest
from database import Connection
from database.tables.autorlivro import AutorLivroTable

class TestAutorLivroTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.autorlivro_table = AutorLivroTable(cls.connection)

    def test_create_autorlivro(self):
        isbn_liv = "9781686923500"  
        autor_liv = "Teste Autor"  
        self.autorlivro_table.create(autor_liv, isbn_liv)
        cursor = self.autorlivro_table.conn.cursor()
        cursor.execute("SELECT AutorLiv, ISBNLiv FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv, isbn_liv))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], autor_liv)
        self.assertEqual(result[1], isbn_liv)
        self.autorlivro_table.delete(autor_liv, isbn_liv)

    def test_create_autorlivro_conflict(self):
        isbn_liv = "9781686923500"
        autor_liv = "Eloá Oliveira"  
        self.autorlivro_table.create(autor_liv, isbn_liv)
        cursor = self.autorlivro_table.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv, isbn_liv))
        count = cursor.fetchone()[0]
        cursor.close()
        self.assertEqual(count, 1)  


    def test_read_autorlivro(self):
        result = self.autorlivro_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertTrue(result["total_registros"] >= 45) 
        self.assertTrue("total_paginas" in result)

    def test_read_autorlivro_with_filter(self):
        isbn_liv = "9781686923500"
        autor_liv = "Eloá Oliveira"  
        result = self.autorlivro_table.read(filter={"AutorLiv": autor_liv, "ISBNLiv": isbn_liv})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], autor_liv)
        self.assertEqual(result["registros"][0][1], isbn_liv)

    def test_update_autorlivro(self):
        isbn_liv_old = "9781686923500"
        autor_liv_old = "Teste Autor"
        isbn_liv_new = "9780066096179"  
        autor_liv_new = "Autor Novo"  
        self.autorlivro_table.create(autor_liv_old, isbn_liv_old)
        self.autorlivro_table.update(autor_liv_old, isbn_liv_old, autor_liv_new, isbn_liv_new)
        cursor = self.autorlivro_table.conn.cursor()
        cursor.execute("SELECT AutorLiv, ISBNLiv FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv_new, isbn_liv_new))
        result_new = cursor.fetchone()
        cursor.execute("SELECT AutorLiv, ISBNLiv FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv_old, isbn_liv_old))
        result_old = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result_new)
        self.assertIsNone(result_old)
        self.assertEqual(result_new[0], autor_liv_new)
        self.assertEqual(result_new[1], isbn_liv_new)
        self.autorlivro_table.delete(autor_liv_new, isbn_liv_new)

    def test_update_autorlivro_inexistente(self):
        isbn_liv_old = "9781686923500"
        autor_liv_old = "Autor Inexistente"
        isbn_liv_new = "9780066096179"
        autor_liv_new = "Autor Novo"
        self.autorlivro_table.update(autor_liv_old, isbn_liv_old, autor_liv_new, isbn_liv_new)
        cursor = self.autorlivro_table.conn.cursor()
        cursor.execute("SELECT AutorLiv, ISBNLiv FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv_new, isbn_liv_new))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result) 

    def test_delete_autorlivro(self):
        isbn_liv = "9781686923500"
        autor_liv = "Teste Autor"
        self.autorlivro_table.create(autor_liv, isbn_liv)
        self.autorlivro_table.delete(autor_liv, isbn_liv)
        cursor = self.autorlivro_table.conn.cursor()
        cursor.execute("SELECT * FROM AutorLivro WHERE AutorLiv = %s AND ISBNLiv = %s;", 
                       (autor_liv, isbn_liv))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_autorlivro_inexistente(self):
        isbn_liv = "9781686923500"
        autor_liv = "Autor Inexistente"
        self.autorlivro_table.delete(autor_liv, isbn_liv)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.autorlivro_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)