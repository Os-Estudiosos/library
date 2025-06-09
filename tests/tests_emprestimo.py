import unittest
from database import Connection
from database.tables.emprestimo import EmprestimoTable
from datetime import date

class TestEmprestimoTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco de dados
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.emprestimo_table = EmprestimoTable(cls.connection)

    def get_next_id(self):
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT MAX(IdEmp) FROM Emprestimo;")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return (max_id or 0) + 1

    def test_create_emprestimo(self):
        # Testa a inserção de um novo empréstimo
        id_emp = self.get_next_id()
        matricula_al = "045"  # Matrícula existente
        isbn_liv = "9781686923500"  # ISBN existente
        cpf_att = "18702495694"    # CPF existente
        self.emprestimo_table.create(id_emp, "2023-01-01", "2023-01-15", 0, matricula_al, isbn_liv, cpf_att)
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT IdEmp, DataInicioEmp, DataFimEmp, BaixaEmp, MatriculaAl, ISBNLiv, CPFAtt FROM Emprestimo WHERE IdEmp = %s AND MatriculaAl = %s;", (id_emp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_emp)
        self.assertEqual(result[1], date(2023, 1, 1))
        self.assertEqual(result[2], date(2023, 1, 15))
        self.assertEqual(result[3], 0)
        self.assertEqual(result[4], matricula_al)
        self.assertEqual(result[5], isbn_liv)
        self.assertEqual(result[6], cpf_att)
        # Limpar o registro inserido
        self.emprestimo_table.delete(id_emp, matricula_al)

    def test_create_emprestimo_conflict(self):
        # Testa a inserção com IdEmp e MatriculaAl já existentes (deve atualizar)
        id_emp = self.get_next_id()
        matricula_al = "045"
        isbn_liv = "9781686923500"
        cpf_att = "18702495694"
        self.emprestimo_table.create(id_emp, "2023-01-01", "2023-01-15", 0, matricula_al, isbn_liv, cpf_att)
        self.emprestimo_table.create(id_emp, "2023-02-01", "2023-02-15", 1, matricula_al, isbn_liv, cpf_att)
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT IdEmp, DataInicioEmp, DataFimEmp, BaixaEmp, MatriculaAl, ISBNLiv, CPFAtt FROM Emprestimo WHERE IdEmp = %s AND MatriculaAl = %s;", (id_emp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_emp)
        self.assertEqual(result[1], date(2023, 2, 1))
        self.assertEqual(result[2], date(2023, 2, 15))
        self.assertEqual(result[3], 1)
        self.assertEqual(result[4], matricula_al)
        self.assertEqual(result[5], isbn_liv)
        self.assertEqual(result[6], cpf_att)
        # Limpar o registro inserido
        self.emprestimo_table.delete(id_emp, matricula_al)

    def test_read_emprestimos(self):
        # Testa a leitura com paginação (ex: 2 registros)
        result = self.emprestimo_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), 2)
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)

    def test_read_emprestimos_with_filter(self):
        # Testa a leitura com filtro por IdEmp e MatriculaAl
        id_emp = 1
        matricula_al = "045"  # Registro existente
        result = self.emprestimo_table.read(filter={"IdEmp": id_emp, "MatriculaAl": matricula_al})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], id_emp)
        self.assertEqual(result["registros"][0][4], matricula_al)

    def test_update_emprestimo(self):
        # Testa a atualização de um empréstimo existente
        id_emp = self.get_next_id()
        matricula_al = "045"
        isbn_liv = "9781686923500"
        cpf_att = "18702495694"
        self.emprestimo_table.create(id_emp, "2023-01-01", "2023-01-15", 0, matricula_al, isbn_liv, cpf_att)
        self.emprestimo_table.update(id_emp, "2023-02-01", "2023-02-15", 1, matricula_al, isbn_liv, cpf_att)
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT IdEmp, DataInicioEmp, DataFimEmp, BaixaEmp, MatriculaAl, ISBNLiv, CPFAtt FROM Emprestimo WHERE IdEmp = %s AND MatriculaAl = %s;", (id_emp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_emp)
        self.assertEqual(result[1], date(2023, 2, 1))
        self.assertEqual(result[2], date(2023, 2, 15))
        self.assertEqual(result[3], 1)
        self.assertEqual(result[4], matricula_al)
        self.assertEqual(result[5], isbn_liv)
        self.assertEqual(result[6], cpf_att)
        # Limpar o registro inserido
        self.emprestimo_table.delete(id_emp, matricula_al)

    def test_update_emprestimo_inexistente(self):
        # Testa a atualização de um empréstimo que não existe
        id_emp = 9999
        matricula_al = "045"
        isbn_liv = "9781686923500"
        cpf_att = "18702495694"
        self.emprestimo_table.update(id_emp, "2023-01-01", "2023-01-15", 0, matricula_al, isbn_liv, cpf_att)
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT * FROM Emprestimo WHERE IdEmp = %s AND MatriculaAl = %s;", (id_emp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_emprestimo(self):
        # Testa a exclusão de um empréstimo existente
        id_emp = self.get_next_id()
        matricula_al = "045"
        isbn_liv = "9781686923500"
        cpf_att = "18702495694"
        self.emprestimo_table.create(id_emp, "2023-01-01", "2023-01-15", 0, matricula_al, isbn_liv, cpf_att)
        self.emprestimo_table.delete(id_emp, matricula_al)
        cursor = self.emprestimo_table.conn.cursor()
        cursor.execute("SELECT * FROM Emprestimo WHERE IdEmp = %s AND MatriculaAl = %s;", (id_emp, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_emprestimo_inexistente(self):
        # Testa a exclusão de um empréstimo que não existe
        id_emp = 9999
        matricula_al = "045"
        self.emprestimo_table.delete(id_emp, matricula_al)
        # Não há necessidade de verificar, pois o método já trata o caso

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        if not cls.connection.closed:
            cls.emprestimo_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)