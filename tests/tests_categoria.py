import unittest
from database import Connection
from database.tables.categoria import CategoriaTable
import pandas as pd

class TestCategoriaTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.categoria_table = CategoriaTable(cls.connection)

    def test_create_categoria(self):
        primary_key = {"IdCat": 999}
        colums = {"NomeCat": "Categoria Teste"}
        self.categoria_table.create(primary_key, colums)
        cursor = self.categoria_table.conn.cursor()
        cursor.execute("SELECT IdCat, NomeCat FROM Categoria WHERE IdCat = %s;", (999,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 999)
        self.assertEqual(result[1], "Categoria Teste")
        self.categoria_table.delete(primary_key)

    def test_create_categoria_conflict(self):
        primary_key = {"IdCat": 1}
        colums = {"NomeCat": "Ficção Atualizada"}
        self.categoria_table.create(primary_key, colums)
        cursor = self.categoria_table.conn.cursor()
        cursor.execute("SELECT IdCat, NomeCat FROM Categoria WHERE IdCat = %s;", (1,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "Ficção Atualizada")
        # Restaurar valor original
        self.categoria_table.update({"IdCat": 1}, {"NomeCat": "Ficção"})

    def test_read_categoria(self):
        result = self.categoria_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 7)
        self.assertTrue("total_paginas" in result)
        self.assertTrue("pagina_atual" in result)
        self.assertEqual(list(result["registros"].columns), ["ID Categoria", "Nome Categoria"])

    def test_read_categoria_with_filter(self):
        filter_dict = {"IdCat": 1}
        result = self.categoria_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["ID Categoria"], 1)
        self.assertEqual(result["registros"].iloc[0]["Nome Categoria"], "Ficção")

    def test_update_categoria(self):
        primary_key = {"IdCat": 999}
        colums_create = {"NomeCat": "Categoria Teste"}
        self.categoria_table.create(primary_key, colums_create)
        colums_update = {"NomeCat": "Categoria Atualizada"}
        self.categoria_table.update(primary_key, colums_update)
        cursor = self.categoria_table.conn.cursor()
        cursor.execute("SELECT IdCat, NomeCat FROM Categoria WHERE IdCat = %s;", (999,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 999)
        self.assertEqual(result[1], "Categoria Atualizada")
        self.categoria_table.delete(primary_key)

    def test_update_categoria_inexistente(self):
        primary_key = {"IdCat": 998}
        colums = {"NomeCat": "Categoria Inexistente"}
        self.categoria_table.update(primary_key, colums)
        cursor = self.categoria_table.conn.cursor()
        cursor.execute("SELECT IdCat, NomeCat FROM Categoria WHERE IdCat = %s;", (998,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_categoria(self):
        primary_key = {"IdCat": 999}
        colums = {"NomeCat": "Categoria Teste"}
        self.categoria_table.create(primary_key, colums)
        self.categoria_table.delete(primary_key)
        cursor = self.categoria_table.conn.cursor()
        cursor.execute("SELECT IdCat, NomeCat FROM Categoria WHERE IdCat = %s;", (999,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_categoria_inexistente(self):
        primary_key = {"IdCat": 998}
        self.categoria_table.delete(primary_key)

    @classmethod
    def tearDownClass(cls):
        cursor = cls.connection.cursor()
        cursor.execute("DELETE FROM Categoria WHERE IdCat = %s;", (999,))
        cls.connection.commit()
        cursor.close()
        if cls.connection and not cls.connection.closed:
            cls.categoria_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)