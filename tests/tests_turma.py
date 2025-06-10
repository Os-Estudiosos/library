import unittest
from database import Connection
from database.tables.turma import TurmaTable
import pandas as pd

class TestTurmaTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco de dados
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais, host ou esquema.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.turma_table = TurmaTable(cls.connection)

    def test_create_turma(self):
        # Testa a inserção de uma nova turma
        primary_key = {"IdTurma": 4}
        colums = {"NomeTurma": "Turma Teste"}
        self.turma_table.create(primary_key, colums)
        cursor = self.turma_table.conn.cursor()
        cursor.execute("SELECT IdTurma, NomeTurma FROM Turma WHERE IdTurma = %s;", (4,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 4)
        self.assertEqual(result[1], "Turma Teste")
        # Limpar o registro inserido
        self.turma_table.delete(primary_key)

    def test_create_turma_conflict(self):
        # Testa a inserção de uma turma existente (atualização via ON CONFLICT)
        primary_key = {"IdTurma": 1}
        colums = {"NomeTurma": "Turma Atualizada"}
        self.turma_table.create(primary_key, colums)
        cursor = self.turma_table.conn.cursor()
        cursor.execute("SELECT IdTurma, NomeTurma FROM Turma WHERE IdTurma = %s;", (1,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Turma Atualizada")
        # Restaurar o registro original
        original_colums = {"NomeTurma": "Turma A"}
        self.turma_table.create(primary_key, original_colums)

    def test_read_turma(self):
        # Testa a leitura com paginação (ex.: 2 registros)
        result = self.turma_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 3)  # Verifica o total de linhas
        self.assertTrue("total_paginas" in result)
        self.assertTrue("pagina_atual" in result)
        self.assertEqual(list(result["registros"].columns), ["ID Turma", "Nome Turma"])

    def test_read_turma_with_filter(self):
        # Testa a leitura com filtro por IdTurma
        filter_dict = {"IdTurma": 1}
        result = self.turma_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["ID Turma"], 1)
        self.assertEqual(result["registros"].iloc[0]["Nome Turma"], "Turma A")

    def test_update_turma(self):
        # Testa a atualização de uma turma existente
        primary_key = {"IdTurma": 4}
        colums_create = {"NomeTurma": "Turma Teste"}
        self.turma_table.create(primary_key, colums_create)
        colums_update = {"NomeTurma": "Turma Nova"}
        self.turma_table.update(primary_key, colums_update)
        cursor = self.turma_table.conn.cursor()
        cursor.execute("SELECT IdTurma, NomeTurma FROM Turma WHERE IdTurma = %s;", (4,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Turma Nova")
        # Limpar o registro inserido
        self.turma_table.delete(primary_key)

    def test_update_turma_inexistente(self):
        # Testa a atualização de uma turma inexistente
        primary_key = {"IdTurma": 999}
        colums = {"NomeTurma": "Turma Inexistente"}
        self.turma_table.update(primary_key, colums)
        cursor = self.turma_table.conn.cursor()
        cursor.execute("SELECT IdTurma FROM Turma WHERE IdTurma = %s;", (999,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_turma(self):
        # Testa a exclusão de uma turma existente
        primary_key = {"IdTurma": 4}
        colums = {"NomeTurma": "Turma Teste"}
        self.turma_table.create(primary_key, colums)
        self.turma_table.delete(primary_key)
        cursor = self.turma_table.conn.cursor()
        cursor.execute("SELECT IdTurma FROM Turma WHERE IdTurma = %s;", (4,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_turma_inexistente(self):
        # Testa a exclusão de uma turma inexistente
        primary_key = {"IdTurma": 999}
        self.turma_table.delete(primary_key)
        # Não há necessidade de verificar, pois o método já trata o caso

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        if cls.connection and not cls.connection.closed:
            cls.turma_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)