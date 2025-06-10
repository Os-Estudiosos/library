import unittest
from database import Connection
from database.tables.categoria import CategoriaTable

class TestCategoriaTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.categoria_table = CategoriaTable(cls.connection)

    def get_next_id(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(IdCat) FROM Categoria;")
        max_id = cursor.fetchone()[0]
        return (max_id or 0) + 1

    def test_create_categoria(self):
        next_id = self.get_next_id()
        self.categoria_table.create(next_id, "Categoria Teste")
        cursor = self.connection.cursor()
        cursor.execute("SELECT NomeCat FROM Categoria WHERE IdCat = %s;", (next_id,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Categoria Teste")
        self.categoria_table.delete(next_id)

    def test_create_categoria_conflict(self):
        next_id = self.get_next_id()
        self.categoria_table.create(next_id, "Categoria Teste A")
        self.categoria_table.create(next_id, "Categoria Teste B") 
        cursor = self.connection.cursor()
        cursor.execute("SELECT NomeCat FROM Categoria WHERE IdCat = %s;", (next_id,))
        result = cursor.fetchone()
        self.assertEqual(result[0], "Categoria Teste B")
        self.categoria_table.delete(next_id)

    def test_read_categorias(self):
        ids = []
        for i in range(3): 
            next_id = self.get_next_id()
            self.categoria_table.create(next_id, f"Categoria Teste {i}")
            ids.append(next_id)
        for id_cat in ids:
            self.categoria_table.delete(id_cat)

    def test_read_categorias_with_filter(self):
        next_id = self.get_next_id()
        self.categoria_table.create(next_id, "Categoria Filtro")
        result = self.categoria_table.read(filter={"IdCat": next_id})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], next_id)
        self.assertEqual(result["registros"][0][1], "Categoria Filtro")
        # Limpar
        self.categoria_table.delete(next_id)

    def test_read_invalid_qtd(self):
        result = self.categoria_table.read(qtd=0)
        self.assertEqual(result, {})  

    def test_update_categoria(self):
        next_id = self.get_next_id()
        self.categoria_table.create(next_id, "Categoria Original")
        self.categoria_table.update(next_id, "Categoria Atualizada")
        cursor = self.connection.cursor()
        cursor.execute("SELECT NomeCat FROM Categoria WHERE IdCat = %s;", (next_id,))
        result = cursor.fetchone()
        self.assertEqual(result[0], "Categoria Atualizada")
        # Limpar
        self.categoria_table.delete(next_id)

    def test_update_categoria_inexistente(self):
        non_existent_id = self.get_next_id() + 1000  
        self.categoria_table.update(non_existent_id, "Categoria Inexistente")
        cursor = self.connection.cursor()
        cursor.execute("SELECT NomeCat FROM Categoria WHERE IdCat = %s;", (non_existent_id,))
        result = cursor.fetchone()
        self.assertIsNone(result) 

    def test_delete_categoria(self):
        next_id = self.get_next_id()
        self.categoria_table.create(next_id, "Categoria a Deletar")
        self.categoria_table.delete(next_id)
        cursor = self.connection.cursor()
        cursor.execute("SELECT NomeCat FROM Categoria WHERE IdCat = %s;", (next_id,))
        result = cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_categoria_inexistente(self):
        non_existent_id = self.get_next_id() + 1000  
        self.categoria_table.delete(non_existent_id)
        
    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.categoria_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)