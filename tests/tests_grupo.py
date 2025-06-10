import unittest
from database import Connection
from database.tables.grupo import GrupoTable

class TestGrupoTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.grupo_table = GrupoTable(cls.connection)

    def get_next_id(self):
        cursor = self.grupo_table.conn.cursor() 
        cursor.execute("SELECT MAX(IdGru) FROM Grupo;") 
        max_id = cursor.fetchone()[0]  
        cursor.close()  
        return (max_id or 0) + 1 

    def test_create_grupo(self):
        next_id = self.get_next_id()
        self.grupo_table.create(next_id, "Grupo Teste")
        cursor = self.grupo_table.conn.cursor()
        cursor.execute("SELECT NomeGru FROM Grupo WHERE IdGru = %s;", (next_id,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Grupo Teste")
        self.grupo_table.delete(next_id)  

    def test_create_grupo_conflict(self):
        next_id = self.get_next_id()
        self.grupo_table.create(next_id, "Grupo Conflito")
        self.grupo_table.create(next_id, "Grupo Conflito Atualizado") 
        cursor = self.grupo_table.conn.cursor()
        cursor.execute("SELECT NomeGru FROM Grupo WHERE IdGru = %s;", (next_id,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Grupo Conflito Atualizado")
        self.grupo_table.delete(next_id)  

    def test_read_grupos(self):
        ids = []
        for i in range(3):
            next_id = self.get_next_id()
            self.grupo_table.create(next_id, f"Grupo Teste {i}")
            ids.append(next_id)
        result = self.grupo_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), 2)
        for id in ids:
            self.grupo_table.delete(id)

    def test_read_grupos_with_filter(self):
        next_id = self.get_next_id()
        self.grupo_table.create(next_id, "Grupo Filtro")
        result = self.grupo_table.read(filter={"IdGru": next_id})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], next_id)
        self.grupo_table.delete(next_id)

    def test_update_grupo(self):
        next_id = self.get_next_id()
        self.grupo_table.create(next_id, "Grupo Original")
        self.grupo_table.update(next_id, "Grupo Atualizado")
        cursor = self.grupo_table.conn.cursor()
        cursor.execute("SELECT NomeGru FROM Grupo WHERE IdGru = %s;", (next_id,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Grupo Atualizado")
        self.grupo_table.delete(next_id)

    def test_delete_grupo(self):
        next_id = self.get_next_id()
        self.grupo_table.create(next_id, "Grupo Delete")
        self.grupo_table.delete(next_id)
        cursor = self.grupo_table.conn.cursor()
        cursor.execute("SELECT NomeGru FROM Grupo WHERE IdGru = %s;", (next_id,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_update_grupo_inexistente(self):
        non_existent_id = self.get_next_id() + 1000
        self.grupo_table.update(non_existent_id, "Grupo Inexistente")
        cursor = self.grupo_table.conn.cursor()
        cursor.execute("SELECT NomeGru FROM Grupo WHERE IdGru = %s;", (non_existent_id,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.grupo_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)