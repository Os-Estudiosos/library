import unittest
from database import Connection
from database.tables.aluno import AlunoTable
import pandas as pd
from datetime import date

class TestAlunoTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.aluno_table = AlunoTable(cls.connection)

    def test_create_aluno(self):
        primary_key = {"MatriculaAl": "099"}
        colums = {
            "PrimeiroNomeAl": "Teste",
            "UltimoNomeAl": "Aluno",
            "DataNascimentoAl": "2000-01-01",
            "SenhaAl": "Teste123!",
            "IdTurma": 1
        }
        self.aluno_table.create(primary_key, colums)
        cursor = self.aluno_table.conn.cursor()
        cursor.execute("SELECT MatriculaAl, PrimeiroNomeAl, UltimoNomeAl, DataNascimentoAl, SenhaAl, IdTurma FROM Aluno WHERE MatriculaAl = %s;", 
                       ("099",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "099")
        self.assertEqual(result[1], "Teste")
        self.assertEqual(result[2], "Aluno")
        self.assertEqual(result[3], date(2000, 1, 1))
        self.assertEqual(result[4], "Teste123!")
        self.assertEqual(result[5], 1)

        self.aluno_table.delete(primary_key)

    def test_create_aluno_conflict(self):
        primary_key = {"MatriculaAl": "001"}
        colums = {
            "PrimeiroNomeAl": "Ana",
            "UltimoNomeAl": "Teste",
            "DataNascimentoAl": "2003-08-28",
            "SenhaAl": "Novo123!",
            "IdTurma": 2
        }
        self.aluno_table.create(primary_key, colums)
        cursor = self.aluno_table.conn.cursor()
        cursor.execute("SELECT MatriculaAl, PrimeiroNomeAl, UltimoNomeAl, DataNascimentoAl, SenhaAl, IdTurma FROM Aluno WHERE MatriculaAl = %s;", 
                       ("001",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "001")
        self.assertEqual(result[2], "Teste")
        self.assertEqual(result[4], "Novo123!") 
        original_colums = {
            "PrimeiroNomeAl": "Ana",
            "UltimoNomeAl": "Lopes",
            "DataNascimentoAl": "2003-08-28",
            "SenhaAl": "#7B&zUdD",
            "IdTurma": 2
        }
        self.aluno_table.create(primary_key, original_colums)

    def test_read_aluno(self):
        result = self.aluno_table.read(qtd=2)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertEqual(result["total_registros"], 84) 
        self.assertTrue("total_paginas" in result)
        self.assertEqual(list(result["registros"].columns), ["Matrícula", "Nome completo", "Data nascimento", "Turma"])

    def test_read_aluno_with_filter(self):
        filter_dict = {"MatriculaAl": "001"}
        result = self.aluno_table.read(filter=filter_dict)
        self.assertIsInstance(result["registros"], pd.DataFrame)
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"].iloc[0]["Matrícula"], "001")
        self.assertEqual(result["registros"].iloc[0]["Nome completo"], "Ana Lopes")
        self.assertEqual(result["registros"].iloc[0]["Data nascimento"], date(2003, 8, 28))

    def test_update_aluno(self):
        primary_key = {"MatriculaAl": "099"}
        colums_create = {
            "PrimeiroNomeAl": "Teste",
            "UltimoNomeAl": "Aluno",
            "DataNascimentoAl": "2000-01-01",
            "SenhaAl": "Teste123!",
            "IdTurma": 1
        }
        self.aluno_table.create(primary_key, colums_create)
        colums_update = {
            "PrimeiroNomeAl": "Novo",
            "UltimoNomeAl": "Teste",
            "DataNascimentoAl": "2001-02-02",
            "SenhaAl": "Novo456!",
            "IdTurma": 2
        }
        self.aluno_table.update(primary_key, colums_update)
        cursor = self.aluno_table.conn.cursor()
        cursor.execute("SELECT MatriculaAl, PrimeiroNomeAl, UltimoNomeAl, DataNascimentoAl, SenhaAl, IdTurma FROM Aluno WHERE MatriculaAl = %s;", 
                       ("099",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Novo")
        self.assertEqual(result[2], "Teste")
        self.assertEqual(result[3], date(2001, 2, 2))
        self.assertEqual(result[4], "Novo456!")
        self.assertEqual(result[5], 2)
        self.aluno_table.delete(primary_key)

    def test_update_aluno_inexistente(self):
        primary_key = {"MatriculaAl": "999"}
        colums = {
            "PrimeiroNomeAl": "Inexistente",
            "UltimoNomeAl": "Teste",
            "DataNascimentoAl": "2000-01-01",
            "SenhaAl": "Teste123!",
            "IdTurma": 1
        }
        self.aluno_table.update(primary_key, colums)
        cursor = self.aluno_table.conn.cursor()
        cursor.execute("SELECT MatriculaAl FROM Aluno WHERE MatriculaAl = %s;", ("999",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_aluno(self):
        primary_key = {"MatriculaAl": "099"}
        colums = {
            "PrimeiroNomeAl": "Teste",
            "UltimoNomeAl": "Aluno",
            "DataNascimentoAl": "2000-01-01",
            "SenhaAl": "Teste123!",
            "IdTurma": 1
        }
        self.aluno_table.create(primary_key, colums)
        self.aluno_table.delete(primary_key)
        cursor = self.aluno_table.conn.cursor()
        cursor.execute("SELECT MatriculaAl FROM Aluno WHERE MatriculaAl = %s;", ("099",))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_aluno_inexistente(self):
        primary_key = {"MatriculaAl": "999"}
        self.aluno_table.delete(primary_key)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.aluno_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)