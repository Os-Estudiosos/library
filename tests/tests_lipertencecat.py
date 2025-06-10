import unittest
from database import Connection
from database.tables.lipertencecat import LiPertenceCatTable
import pandas as pd

class TestLiPertenceCatTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco de dados
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.lipertencecat_table = LiPertenceCatTable(cls.connection)
        # Inserir registros temporários para chaves estrangeiras
        cursor = cls.connection.cursor()
        # Inserir categoria temporária
        # OBS: Ajuste para IdCatLiv, NomeCatLiv se o DDL de Categoria confirmar
        cursor.execute("""
            INSERT INTO Categoria (IdCat, NomeCat)
            VALUES (%s, %s)
            ON CONFLICT (IdCat) DO NOTHING;
        """, (999, "Categoria Teste"))
        # Inserir livro temporário
        cursor.execute("""
            INSERT INTO Livro (ISBNLiv, NomeLiv, EditoraLiv, EdicaoLiv, AnoLancamentoLiv)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (ISBNLiv) DO NOTHING;
        """, ("9999999999999", "Livro Teste", "Editora Teste", 1, "2023-01-01"))
        cls.connection.commit()
        cursor.close()

    def test_create_lipertencecat(self):
        # Testa a inserção de uma nova relação
        primary_key = {"ISBNLiv": "9999999999999", "IdCat": 999}
        colums = {}
        self.lipertencecat_table.create(primary_key, colums)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;",
                       ("9999999999999", 999))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "9999999999999")
        self.assertEqual(result[1], 999)
        # Limpar o registro inserido
        self.lipertencecat_table.delete(primary_key)

    def test_create_lipertencecat_conflict(self):
        # Testa a inserção de uma relação existente (atualização via ON CONFLICT)
        primary_key = {"ISBNLiv": "9781686923500", "IdCat": 1}
        colums = {}
        self.lipertencecat_table.create(primary_key, colums)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;",
                       ("9781686923500", 1))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "9781686923500")
        self.assertEqual(result[1], 1)


    def test_read_lipertencecat(self):
        result = self.lipertencecat_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)
        self.assertTrue("pagina_atual" in result)
        self.assertEqual(list(result["registros"].columns), ["ISBN Livro", "ID Categoria"])

    def test_read_lipertencecat_with_filter(self):
        # Testa a leitura com filtro por ISBNLiv e IdCat
        filter_dict = {"ISBNLiv": "9781686923500", "IdCat": 1}
        result = self.lipertencecat_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["ISBN Livro"], "9781686923500")
        self.assertEqual(result["registros"].iloc[0]["ID Categoria"], 1)

    def test_update_lipertencecat(self):
        # Testa a atualização de uma relação existente (colums vazio)
        primary_key = {"ISBNLiv": "9999999999999", "IdCat": 999}
        colums_create = {}
        self.lipertencecat_table.create(primary_key, colums_create)
        colums_update = {}
        self.lipertencecat_table.update(primary_key, colums_update)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;",
                       ("9999999999999", 999))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)  # UPDATE com colums vazio não altera
        self.assertEqual(result[0], "9999999999999")
        self.assertEqual(result[1], 999)
        # Limpar o registro
        self.lipertencecat_table.delete(primary_key)

    def test_update_lipertencecat_inexistente(self):
        # Testa a atualização de uma relação inexistente
        primary_key = {"ISBNLiv": "9999999999998", "IdCat": 998}
        colums = {}
        self.lipertencecat_table.update(primary_key, colums)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;",
                       ("9999999999998", 998))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_lipertencecat(self):
        # Testa a exclusão de uma relação existente
        primary_key = {"ISBNLiv": "9999999999999", "IdCat": 999}
        colums = {}
        self.lipertencecat_table.create(primary_key, colums)
        self.lipertencecat_table.delete(primary_key)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;",
                       ("9999999999999", 999))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_lipertencecat_inexistente(self):
        # Testa a exclusão de uma relação inexistente
        primary_key = {"ISBNLiv": "9999999999998", "IdCat": 998}
        self.lipertencecat_table.delete(primary_key)
        # Não há necessidade de verificar, pois o método já trata o caso

    @classmethod
    def tearDownClass(cls):
        # Limpar registros temporários
        cursor = cls.connection.cursor()
        cursor.execute("DELETE FROM LiPertenceCat WHERE ISBNLiv = %s;", ("9999999999999",))
        cursor.execute("DELETE FROM Livro WHERE ISBNLiv = %s;", ("9999999999999",))
        cursor.execute("DELETE FROM Categoria WHERE IdCat = %s;", (999,))
        cls.connection.commit()
        cursor.close()
        # Fecha a conexão
        if cls.connection and not cls.connection.closed:
            cls.lipertencecat_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)