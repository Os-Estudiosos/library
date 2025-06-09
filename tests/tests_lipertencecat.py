import unittest
from database import Connection
from database.tables.lipertencecat import LiPertenceCatTable

class TestLiPertenceCatTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.lipertencecat_table = LiPertenceCatTable(cls.connection)

    def test_create_lipertencecat(self):
        isbn_liv = "9781686923500"  
        id_cat = 7
        self.lipertencecat_table.create(isbn_liv, id_cat)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], isbn_liv)
        self.assertEqual(result[1], id_cat)
        self.lipertencecat_table.delete(isbn_liv, id_cat)

    def test_create_lipertencecat_conflict(self):
        isbn_liv = "9781686923500"
        id_cat = 1 
        self.lipertencecat_table.create(isbn_liv, id_cat)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat))
        count = cursor.fetchone()[0]
        cursor.close()
        self.assertEqual(count, 1)

    def test_read_lipertencecat(self):
        result = self.lipertencecat_table.read(qtd=2)
        self.assertEqual(len(result["registros"]), min(2, result["total_registros"]))
        self.assertTrue("total_registros" in result)
        self.assertTrue(result["total_registros"] >= 107) 
        self.assertTrue("total_paginas" in result)

    def test_read_lipertencecat_with_filter(self):
        isbn_liv = "9781686923500"
        id_cat = 1 
        result = self.lipertencecat_table.read(filter={"ISBNLiv": isbn_liv, "IdCat": id_cat})
        self.assertEqual(len(result["registros"]), 1)
        self.assertEqual(result["registros"][0][0], isbn_liv)
        self.assertEqual(result["registros"][0][1], id_cat)

    def test_update_lipertencecat(self):
        isbn_liv = "9781686923500"
        id_cat_old = 6
        id_cat_new = 7 
        self.lipertencecat_table.create(isbn_liv, id_cat_old)
        self.lipertencecat_table.update(isbn_liv, id_cat_old, id_cat_new)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat_new))
        result_new = cursor.fetchone()
        cursor.execute("SELECT ISBNLiv, IdCat FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat_old))
        result_old = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result_new)
        self.assertIsNone(result_old)
        self.assertEqual(result_new[0], isbn_liv)
        self.assertEqual(result_new[1], id_cat_new)
        self.lipertencecat_table.delete(isbn_liv, id_cat_new)

    def test_update_lipertencecat_inexistente(self):
        isbn_liv = "9781686923500"
        id_cat_old = 999
        id_cat_new = 7
        self.lipertencecat_table.update(isbn_liv, id_cat_old, id_cat_new)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT * FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat_new))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_lipertencecat(self):
        isbn_liv = "9781686923500"
        id_cat = 7
        self.lipertencecat_table.create(isbn_liv, id_cat)
        self.lipertencecat_table.delete(isbn_liv, id_cat)
        cursor = self.lipertencecat_table.conn.cursor()
        cursor.execute("SELECT * FROM LiPertenceCat WHERE ISBNLiv = %s AND IdCat = %s;", 
                       (isbn_liv, id_cat))
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNone(result)

    def test_delete_lipertencecat_inexistente(self):
        isbn_liv = "9781686923500"
        id_cat = 999
        self.lipertencecat_table.delete(isbn_liv, id_cat)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.lipertencecat_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)