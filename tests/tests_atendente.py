import unittest
from database import Connection
from database.tables.atendente import AtendenteTable
import pandas as pd

class TestAtendenteTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco de dados
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais, host ou esquema.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.atendente_table = AtendenteTable(cls.connection)

    def test_create_atendente(self):
        # Testa a inserção de um novo atendente
        primary_key = {"CPFAtt": "12345678901"}
        colums = {
            "PrimeiroNomeAtt": "Teste",
            "UltimoNomeAtt": "Atendente"
        }
        self.atendente_table.create(primary_key, colums)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT CPFAtt, PrimeiroNomeAtt, UltimoNomeAtt FROM Atendente WHERE CPFAtt = %s;", 
                       ("12345678901",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "12345678901")
        self.assertEqual(result[1], "Teste")
        self.assertEqual(result[2], "Atendente")
        # Limpar o registro inserido
        self.atendente_table.delete(primary_key)

    def test_create_atendente_conflict(self):
        # Testa a inserção de um atendente existente (atualização via ON CONFLICT)
        primary_key = {"CPFAtt": "18702495694"}
        colums = {
            "PrimeiroNomeAtt": "Asafe",
            "UltimoNomeAtt": "Teste"
        }
        self.atendente_table.create(primary_key, colums)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT CPFAtt, PrimeiroNomeAtt, UltimoNomeAtt FROM Atendente WHERE CPFAtt = %s;", 
                       ("18702495694",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "18702495694")
        self.assertEqual(result[2], "Teste")  # UltimoNomeAtt atualizado
        # Restaurar o registro original
        original_colums = {
            "PrimeiroNomeAtt": "Asafe",
            "UltimoNomeAtt": "Martins"
        }
        self.atendente_table.create(primary_key, original_colums)

    def test_read_atendente(self):
        # Testa a leitura com paginação (ex.: 2 registros)
        result = self.atendente_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 5)  # Verifica o total de linhas
        self.assertTrue("total_paginas" in result)
        self.assertEqual(list(result["registros"].columns), ["CPF", "Nome completo"])

    def test_read_atendente_with_filter(self):
        # Testa a leitura com filtro por CPFAtt
        filter_dict = {"CPFAtt": "18702495694"}
        result = self.atendente_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["CPF"], "18702495694")
        self.assertEqual(result["registros"].iloc[0]["Nome completo"], "Asafe Martins")

    def test_update_atendente(self):
        # Testa a atualização de um atendente existente
        primary_key = {"CPFAtt": "12345678901"}
        colums_create = {
            "PrimeiroNomeAtt": "Teste",
            "UltimoNomeAtt": "Atendente"
        }
        self.atendente_table.create(primary_key, colums_create)
        colums_update = {
            "PrimeiroNomeAtt": "Novo",
            "UltimoNomeAtt": "Teste"
        }
        self.atendente_table.update(primary_key, colums_update)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT CPFAtt, PrimeiroNomeAtt, UltimoNomeAtt FROM Atendente WHERE CPFAtt = %s;", 
                       ("12345678901",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Novo")
        self.assertEqual(result[2], "Teste")
        # Limpar o registro inserido
        self.atendente_table.delete(primary_key)

    def test_update_atendente_inexistente(self):
        # Testa a atualização de um atendente inexistente
        primary_key = {"CPFAtt": "99999999999"}
        colums = {
            "PrimeiroNomeAtt": "Inexistente",
            "UltimoNomeAtt": "Teste"
        }
        self.atendente_table.update(primary_key, colums)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT CPFAtt FROM Atendente WHERE CPFAtt = %s;", ("99999999999",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_atendente(self):
        # Testa a exclusão de um atendente existente
        primary_key = {"CPFAtt": "12345678901"}
        colums = {
            "PrimeiroNomeAtt": "Teste",
            "UltimoNomeAtt": "Atendente"
        }
        self.atendente_table.create(primary_key, colums)
        self.atendente_table.delete(primary_key)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT CPFAtt FROM Atendente WHERE CPFAtt = %s;", ("12345678901",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_atendente_inexistente(self):
        # Testa a exclusão de um atendente inexistente
        primary_key = {"CPFAtt": "99999999999"}
        self.atendente_table.delete(primary_key)
        # Não há necessidade de verificar, pois o método já trata o caso

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        if cls.connection and not cls.connection.closed:
            cls.atendente_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)