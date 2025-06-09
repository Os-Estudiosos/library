import unittest
from database import Connection
from database.tables.suspensao import SuspensaoTable
from datetime import date

class TestSuspensaoTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco de dados
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.suspensao_table = SuspensaoTable(cls.connection)

    def get_next_id(self):
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT MAX(IdSusp) FROM Suspensao;")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return (max_id or 0) + 1

    def test_create_suspensao(self):
        # Testa a inserção de uma nova suspensão
        id_susp = self.get_next_id()
        matricula_al = "004"  # Matrícula existente
        self.suspensao_table.create(id_susp, "2024-01-01", "2024-01-15", matricula_al)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, DataInicioSusp, DataFimSusp, MatriculaAl FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (id_susp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_susp)
        self.assertEqual(result[1], date(2024, 1, 1))
        self.assertEqual(result[2], date(2024, 1, 15))
        self.assertEqual(result[3], matricula_al)
        # Limpar o registro inserido
        self.suspensao_table.delete(id_susp, matricula_al)

    def test_create_suspensao_conflict(self):
        # Testa a inserção com IdSusp e MatriculaAl já existentes (deve atualizar)
        id_susp = self.get_next_id()
        matricula_al = "004"
        self.suspensao_table.create(id_susp, "2024-01-01", "2024-01-15", matricula_al)
        self.suspensao_table.create(id_susp, "2024-02-01", "2024-02-15", matricula_al)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, DataInicioSusp, DataFimSusp, MatriculaAl FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (id_susp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_susp)
        self.assertEqual(result[1], date(2024, 2, 1))
        self.assertEqual(result[2], date(2024, 2, 15))
        self.assertEqual(result[3], matricula_al)
        # Limpar o registro inserido
        self.suspensao_table.delete(id_susp, matricula_al)

    def test_read_suspensoes(self):
        # Testa a leitura com paginação (ex.: 2 registros)
        result = self.suspensao_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)

    def test_read_suspensoes_with_filter(self):
        # Testa a leitura com filtro por IdSusp e MatriculaAl
        id_susp = 1
        matricula_al = "004"  # Registro existente
        result = self.suspensao_table.read(filter={"IdSusp": id_susp, "MatriculaAl": matricula_al})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], id_susp)
        self.assertEqual(result["registros"][0][3], matricula_al)

    def test_update_suspensao(self):
        # Testa a atualização de uma suspensão existente
        id_susp = self.get_next_id()
        matricula_al = "004"
        self.suspensao_table.create(id_susp, "2024-01-01", "2024-01-15", matricula_al)
        self.suspensao_table.update(id_susp, "2024-02-05", "2024-02-20", matricula_al)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT IdSusp, DataInicioSusp, DataFimSusp, MatriculaAl FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", 
                       (id_susp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_susp)
        self.assertEqual(result[1], date(2024, 2, 5))
        self.assertEqual(result[2], date(2024, 2, 20))
        self.assertEqual(result[3], matricula_al)
        # Limpar o registro inserido
        self.suspensao_table.delete(id_susp, matricula_al)

    def test_update_suspensao_inexistente(self):
        # Testa a atualização de uma suspensão que não existe
        id_susp = 9999
        matricula_al = "004"
        self.suspensao_table.update(id_susp, "2024-06-01", "2024-06-15", matricula_al)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT * FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", (id_susp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_suspensao(self):
        # Testa a exclusão de uma suspensão existente
        id_susp = self.get_next_id()
        matricula_al = "004"
        self.suspensao_table.create(id_susp, "2024-01-01", "2024-01-15", matricula_al)
        self.suspensao_table.delete(id_susp, matricula_al)
        cursor = self.suspensao_table.conn.cursor()
        cursor.execute("SELECT * FROM Suspensao WHERE IdSusp = %s AND MatriculaAl = %s;", (id_susp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_suspensao_inexistente(self):
        # Testa a exclusão de uma suspensão que não existe
        id_susp = 9999
        matricula_al = "004"
        self.suspensao_table.delete(id_susp, matricula_al)
        # Não há necessidade de verificar, pois o método já trata o caso

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        if not cls.connection.closed:
            cls.suspensao_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)