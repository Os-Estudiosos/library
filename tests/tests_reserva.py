import unittest
from database import Connection
from database.tables.reserva import ReservaTable
from datetime import date

class TestReservaTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.reserva_table = ReservaTable(cls.connection)

    def get_next_id(self):
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT MAX(IdRes) FROM Reserva;")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return (max_id or 0) + 1

    def test_create_reserva(self):
        id_res = self.get_next_id()
        matricula_al = "004"  
        isbn_liv = "9781686923500" 
        self.reserva_table.create(id_res, "2024-01-01", matricula_al, isbn_liv)
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT IdRes, DataRes, MatriculaAl, ISBNLiv FROM Reserva WHERE IdRes = %s AND MatriculaAl = %s;", 
                       (id_res, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_res)
        self.assertEqual(result[1], date(2024, 1, 1))
        self.assertEqual(result[2], matricula_al)
        self.assertEqual(result[3], isbn_liv)
        self.reserva_table.delete(id_res, matricula_al)

    def test_create_reserva_conflict(self):
        id_res = self.get_next_id()
        matricula_al = "004"
        isbn_liv = "9781686923500"
        self.reserva_table.create(id_res, "2024-01-01", matricula_al, isbn_liv)
        self.reserva_table.create(id_res, "2024-02-01", matricula_al, isbn_liv)
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT IdRes, DataRes, MatriculaAl, ISBNLiv FROM Reserva WHERE IdRes = %s AND MatriculaAl = %s;", 
                       (id_res, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_res)
        self.assertEqual(result[1], date(2024, 2, 1))
        self.assertEqual(result[2], matricula_al)
        self.assertEqual(result[3], isbn_liv)
        self.reserva_table.delete(id_res, matricula_al)

    def test_read_reservas(self):
        result = self.reserva_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertTrue("total_paginas" in result)

    def test_read_reservas_with_filter(self):
        id_res = 1  
        matricula_al = "004"
        result = self.reserva_table.read(filter={"IdRes": id_res, "MatriculaAl": matricula_al})
        self.assertTrue(len(result["registros"]) <= 1)
        if result["registros"]:
            self.assertEqual(result["registros"][0][0], id_res)
            self.assertEqual(result["registros"][0][2], matricula_al)

    def test_update_reserva(self):
        id_res = self.get_next_id()
        matricula_al = "004"
        isbn_liv = "9781686923500"
        self.reserva_table.create(id_res, "2024-01-01", matricula_al, isbn_liv)
        self.reserva_table.update(id_res, "2024-02-05", matricula_al, isbn_liv)
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT IdRes, DataRes, MatriculaAl, ISBNLiv FROM Reserva WHERE IdRes = %s AND MatriculaAl = %s;", 
                       (id_res, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], id_res)
        self.assertEqual(result[1], date(2024, 2, 5))
        self.assertEqual(result[2], matricula_al)
        self.assertEqual(result[3], isbn_liv)
        self.reserva_table.delete(id_res, matricula_al)

    def test_update_reserva_inexistente(self):
        id_res = 9999
        matricula_al = "004"
        isbn_liv = "9781686923500"
        self.reserva_table.update(id_res, "2024-06-01", matricula_al, isbn_liv)
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE IdRes = %s AND MatriculaAl = %s;", (id_res, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_reserva(self):
        id_res = self.get_next_id()
        matricula_al = "004"
        isbn_liv = "9781686923500"
        self.reserva_table.create(id_res, "2024-01-01", matricula_al, isbn_liv)
        self.reserva_table.delete(id_res, matricula_al)
        cursor = self.reserva_table.conn.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE IdRes = %s AND MatriculaAl = %s;", (id_res, matricula_al))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_reserva_inexistente(self):
        id_res = 9999
        matricula_al = "004"
        self.reserva_table.delete(id_res, matricula_al)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.reserva_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)