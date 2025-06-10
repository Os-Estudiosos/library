import unittest
from database import Connection
from database.tables.suspensao import SuspensaoTable
import pandas as pd
from datetime import date

class TestSuspensaoTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        if cls.connection is None:
            raise RuntimeError("Falha ao inicializar a conexão com o banco de dados. Verifique as credenciais, host ou esquema.")
        if cls.connection.closed:
            raise RuntimeError("Conexão com o banco de dados está fechada.")
        cls.suspensao_table = SuspensaoTable(cls.connection)
        cursor = cls.connection.cursor()
        cursor.execute("""
            INSERT INTO Aluno (MatriculaAl, PrimeiroNomeAl, UltimoNomeAl, DataNascimentoAl, SenhaAl, IdTurma)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (MatriculaAl) DO NOTHING;
        """, ('999', 'Teste', 'Aluno', '2000-01-01', 'test123', 1))
        cls.connection.commit()
        cursor.close()

    def test_create_suspensao(self):
        primary_key = {"IdSusp": 9, "MatriculaAl": "999"}
        colums = {
            "DataInicioSusp": "2024-01-01",
            "DataFimSusp": "2024-01-10"
        }
        self.suspensao_table.create(primary_key, colums)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, MatriculaAl, DataInicioSusp, DataFimSusp FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (9, "999"))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 9)
        self.assertEqual(result[1], "999")
        self.assertEqual(result[2], date(2024, 1, 1))
        self.assertEqual(result[3], date(2024, 1, 10))
        self.suspensao_table.delete(primary_key)

    def test_create_suspensao_conflict(self):
        primary_key = {"IdSusp": 1, "MatriculaAl": "004"}
        colums = {
            "DataInicioSusp": "2023-01-01",
            "DataFimSusp": "2023-01-15"
        }
        self.suspensao_table.create(primary_key, colums)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, MatriculaAl, DataInicioSusp, DataFimSusp FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (1, "004"))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[2], date(2023, 1, 1))
        self.assertEqual(result[3], date(2023, 1, 15))
        original_colums = {
            "DataInicioSusp": "2022-12-09",
            "DataFimSusp": "2023-01-02"
        }
        self.suspensao_table.create(primary_key, original_colums)

    def test_read_suspensao(self):
        result = self.suspensao_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 8)
        self.assertTrue("total_paginas" in result)
        self.assertTrue("pagina_atual" in result)
        self.assertEqual(list(result["registros"].columns), ["Id Suspensão", "Data Início", "Data Fim", "Nome Aluno"])

    def test_read_suspensao_with_filter(self):
        filter_dict = {"IdSusp": 1, "MatriculaAl": "004"}
        result = self.suspensao_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["Id Suspensão"], 1)
        self.assertEqual(result["registros"].iloc[0]["Data Início"], date(2022, 12, 9))
        self.assertEqual(result["registros"].iloc[0]["Data Fim"], date(2023, 1, 2))
        self.assertIsNotNone(result["registros"].iloc[0]["Nome Aluno"]) 

    def test_update_suspensao(self):
        primary_key = {"IdSusp": 9, "MatriculaAl": "999"}
        colums_create = {
            "DataInicioSusp": "2024-01-01",
            "DataFimSusp": "2024-01-10"
        }
        self.suspensao_table.create(primary_key, colums_create)
        colums_update = {
            "DataInicioSusp": "2024-02-01",
            "DataFimSusp": "2024-02-15"
        }
        self.suspensao_table.update(primary_key, colums_update)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, MatriculaAl, DataInicioSusp, DataFimSusp FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (9, "999"))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[2], date(2024, 2, 1))
        self.assertEqual(result[3], date(2024, 2, 15))
        self.suspensao_table.delete(primary_key)

    def test_update_suspensao_inexistente(self):
        primary_key = {"IdSusp": 999999999, "MatriculaAl": "999"}
        colums = {
            "DataInicioSusp": "2024-01-01",
            "DataFimSusp": "2024-01-10"
        }
        self.suspensao_table.update(primary_key, colums)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, MatriculaAl FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", (999999999, "999"))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_suspensao(self):
        primary_key = {"IdSusp": 9, "MatriculaAl": "999"}
        colums = {
            "DataInicioSusp": "2024-01-01",
            "DataFimSusp": "2024-01-10"
        }
        self.suspensao_table.create(primary_key, colums)
        self.suspensao_table.delete(primary_key)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, MatriculaAl FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", (9, "999"))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_suspensao_inexistente(self):
        primary_key = {"IdSusp": 999999999, "MatriculaAl": "999"}
        self.suspensao_table.delete(primary_key)

    @classmethod
    def tearDownClass(cls):
        cursor = cls.connection.cursor()
        cursor.execute("DELETE FROM Aluno WHERE MatriculaAl = %s;", ('999',))
        cls.connection.commit()
        cursor.close()
        if cls.connection and not cls.connection.closed:
            cls.suspensao_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)