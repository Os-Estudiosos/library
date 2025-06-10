import unittest
from database import Connection
from database.tables.livro import LivroTable
import pandas as pd
from datetime import date

class TestLivroTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais, host ou esquema.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.livro_table = LivroTable(cls.connection)

    def test_create_livro(self):
        primary_key = {"ISBNLiv": "9781234567890"}
        colums = {
            "NomeLiv": "Teste Livro",
            "EditoraLiv": "Teste Editora",
            "EdicaoLiv": 1,
            "AnoLancamentoLiv": "2023-01-01",
            "IdGru": 6
        }
        self.livro_table.create(primary_key, colums)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", 
                       ("9781234567890",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "9781234567890")
        self.assertEqual(result[1], "Teste Livro")
        self.assertEqual(result[2], "Teste Editora")
        self.assertEqual(result[3], 1)
        self.assertEqual(result[4], date(2023, 1, 1))
        self.assertEqual(result[5], 6)
        self.livro_table.delete(primary_key)

    def test_create_livro_conflict(self):
        primary_key = {"ISBNLiv": "9781686923500"}
        colums = {
            "NomeLiv": "Teste Livro Atualizado",
            "EditoraLiv": "Nova Editora",
            "EdicaoLiv": 2,
            "AnoLancamentoLiv": "2013-01-01",
            "IdGru": 6
        }
        self.livro_table.create(primary_key, colums)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", 
                       ("9781686923500",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "9781686923500")
        self.assertEqual(result[1], "Teste Livro Atualizado")
        self.assertEqual(result[2], "Nova Editora")
        original_colums = {
            "NomeLiv": "Doloremque aspernatur eveniet",
            "EditoraLiv": "Ferreira da Costa Ltda.",
            "EdicaoLiv": 1,
            "AnoLancamentoLiv": "2012-07-15",
            "IdGru": 6
        }
        self.livro_table.create(primary_key, original_colums)

    def test_read_livro(self):
        result = self.livro_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 51)  
        self.assertTrue("total_paginas" in result)
        self.assertTrue("pagina_atual" in result)
        self.assertEqual(list(result["registros"].columns), ["ISBN Livro", "Nome Livro", "Editora Livro", "Edição Livro", "Ano Lançamento", "Grupo"])

    def test_read_livro_with_filter(self):
        filter_dict = {"ISBNLiv": "9781686923500"}
        result = self.livro_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["ISBN Livro"], "9781686923500")
        self.assertEqual(result["registros"].iloc[0]["Nome Livro"], "Doloremque aspernatur eveniet")
        self.assertEqual(result["registros"].iloc[0]["Editora Livro"], "Ferreira da Costa Ltda.")
        self.assertEqual(result["registros"].iloc[0]["Edição Livro"], 1)
        self.assertEqual(result["registros"].iloc[0]["Ano Lançamento"], date(2012, 7, 15))

    def test_update_livro(self):
        primary_key = {"ISBNLiv": "9781234567890"}
        colums_create = {
            "NomeLiv": "Teste Livro",
            "EditoraLiv": "Teste Editora",
            "EdicaoLiv": 1,
            "AnoLancamentoLiv": "2023-01-01",
            "IdGru": 6
        }
        self.livro_table.create(primary_key, colums_create)
        colums_update = {
            "NomeLiv": "Novo Livro",
            "EditoraLiv": "Nova Editora",
            "EdicaoLiv": 2,
            "AnoLancamentoLiv": "2024-01-01",
            "IdGru": 6
        }
        self.livro_table.update(primary_key, colums_update)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv, IdGru FROM Livro WHERE ISBNLiv = %s;", 
                       ("9781234567890",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Novo Livro")
        self.assertEqual(result[2], "Nova Editora")
        self.assertEqual(result[3], 2)
        self.assertEqual(result[4], date(2024, 1, 1))
        self.assertEqual(result[5], 6)
        self.livro_table.delete(primary_key)

    def test_update_livro_inexistente(self):
        primary_key = {"ISBNLiv": "9789999999999"}
        colums = {
            "NomeLiv": "Inexistente",
            "EditoraLiv": "Teste Editora",
            "EdicaoLiv": 1,
            "AnoLancamentoLiv": "2023-01-01",
            "IdGru": 6
        }
        self.livro_table.update(primary_key, colums)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv FROM Livro WHERE ISBNLiv = %s;", ("9789999999999",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_livro(self):
        primary_key = {"ISBNLiv": "9781234567890"}
        colums = {
            "NomeLiv": "Teste Livro",
            "EditoraLiv": "Teste Editora",
            "EdicaoLiv": 1,
            "AnoLancamentoLiv": "2023-01-01",
            "IdGru": 6
        }
        self.livro_table.create(primary_key, colums)
        self.livro_table.delete(primary_key)
        cursor = self.livro_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv FROM Livro WHERE ISBNLiv = %s;", ("9781234567890",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_livro_inexistente(self):
        primary_key = {"ISBNLiv": "9789999999999"}
        self.livro_table.delete(primary_key)

    @classmethod
    def tearDownClass(cls):
        if cls.connection and not cls.connection.closed:
            cls.livro_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)