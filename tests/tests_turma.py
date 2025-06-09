import unittest
from database import Connection
from database.tables.turma import TurmaTable

class TestTurmaTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.turma_table = TurmaTable(cls.connection)

    def get_next_id(self):
        self.turma_table.cursor.execute("SELECT MAX(IdTurma) FROM Turma;")
        max_id = self.turma_table.cursor.fetchone()[0]
        return (max_id or 0) + 1

    def test_create_turma(self):
        next_id = self.get_next_id()
        self.turma_table.create(next_id, "Turma Teste")
        self.turma_table.cursor.execute("SELECT NomeTurma FROM Turma WHERE IdTurma = %s;", (next_id,))
        result = self.turma_table.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Turma Teste")
        self.turma_table.delete(next_id)

    def test_create_turma_conflict(self):
        next_id = self.get_next_id()
        self.turma_table.create(next_id, "Turma Teste A")
        self.turma_table.create(next_id, "Turma Teste B")  # Deve atualizar devido ao ON CONFLICT
        self.turma_table.cursor.execute("SELECT NomeTurma FROM Turma WHERE IdTurma = %s;", (next_id,))
        result = self.turma_table.cursor.fetchone()
        self.assertEqual(result[0], "Turma Teste B")
        # Limpar
        self.turma_table.delete(next_id)

    def test_read_turmas(self):
        ids = []
        for i in range(3):
            next_id = self.get_next_id()
            self.turma_table.create(next_id, f"Turma Teste {i}")
            ids.append(next_id)
        result = self.turma_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), 2)
        # Limpar
        for id in ids:
            self.turma_table.delete(id)

    def test_read_turmas_with_filter(self):
        next_id = self.get_next_id()
        self.turma_table.create(next_id, "Turma Filtro")
        result = self.turma_table.read(filter={"IdTurma": next_id})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], next_id)
        self.turma_table.delete(next_id)

    def test_update_turma(self):
        next_id = self.get_next_id()
        self.turma_table.create(next_id, "Turma Original")
        self.turma_table.update(next_id, "Turma Atualizada")
        self.turma_table.cursor.execute("SELECT NomeTurma FROM Turma WHERE IdTurma = %s;", (next_id,))
        result = self.turma_table.cursor.fetchone()
        self.assertEqual(result[0], "Turma Atualizada")
        self.turma_table.delete(next_id)

    def test_update_turma_inexistente(self):
        non_existent_id = self.get_next_id() + 1000
        self.turma_table.update(non_existent_id, "Turma Inexistente")
        self.turma_table.cursor.execute("SELECT NomeTurma FROM Turma WHERE IdTurma = %s;", (non_existent_id,))
        result = self.turma_table.cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_turma(self):
        next_id = self.get_next_id()
        self.turma_table.create(next_id, "Turma a Deletar")
        self.turma_table.delete(next_id)
        self.turma_table.cursor.execute("SELECT NomeTurma FROM Turma WHERE IdTurma = %s;", (next_id,))
        result = self.turma_table.cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_turma_inexistente(self):
        non_existent_id = self.get_next_id() + 1000
        self.turma_table.delete(non_existent_id)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.turma_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)