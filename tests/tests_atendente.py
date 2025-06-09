import unittest
from database import Connection
from database.tables.atendente import AtendenteTable

class TestAtendenteTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.atendente_table = AtendenteTable(cls.connection)

    def test_create_atendente(self):
        cpf_teste = "12345678901"
        self.atendente_table.create(cpf_teste, "Teste", "Unitario")
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT primeironomeatt, ultimonomeatt FROM Atendente WHERE cpfatt = %s;", (cpf_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Teste")
        self.assertEqual(result[1], "Unitario")
        self.atendente_table.delete(cpf_teste)

    def test_create_atendente_conflict(self):
        cpf_teste = "12345678901"
        self.atendente_table.create(cpf_teste, "Teste", "Unitario")
        self.atendente_table.create(cpf_teste, "TesteAtualizado", "UnitarioAtualizado")
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT primeironomeatt, ultimonomeatt FROM Atendente WHERE cpfatt = %s;", (cpf_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "TesteAtualizado")
        self.assertEqual(result[1], "UnitarioAtualizado")
        self.atendente_table.delete(cpf_teste)

    def test_read_atendentes(self):
        result = self.atendente_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), 2)
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)

    def test_read_atendentes_with_filter(self):
        cpf_existente = "18702495694"
        result = self.atendente_table.read(filter={"cpfatt": cpf_existente})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], cpf_existente)

    def test_update_atendente(self):
        cpf_teste = "12345678901"
        self.atendente_table.create(cpf_teste, "Teste", "Unitario")
        self.atendente_table.update(cpf_teste, "TesteAtualizado", "UnitarioAtualizado")
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT primeironomeatt, ultimonomeatt FROM Atendente WHERE cpfatt = %s;", (cpf_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "TesteAtualizado")
        self.assertEqual(result[1], "UnitarioAtualizado")
        self.atendente_table.delete(cpf_teste)

    def test_update_atendente_inexistente(self):
        cpf_inexistente = "99999999999"
        self.atendente_table.update(cpf_inexistente, "Nome", "Sobrenome")
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT * FROM Atendente WHERE cpfatt = %s;", (cpf_inexistente,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_atendente(self):
        cpf_teste = "12345678901"
        self.atendente_table.create(cpf_teste, "Teste", "Unitario")
        self.atendente_table.delete(cpf_teste)
        cursor = self.atendente_table.conn.cursor()
        cursor.execute("SELECT * FROM Atendente WHERE cpfatt = %s;", (cpf_teste,))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_atendente_inexistente(self):
        cpf_inexistente = "99999999999"
        self.atendente_table.delete(cpf_inexistente)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.atendente_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)