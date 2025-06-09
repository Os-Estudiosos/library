import unittest
from database import Connection
from database.tables.alfavoritaliv import AlFavoritaLivTable

class TestAlFavoritaLivTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa a conexão com o banco
        cls.connection = Connection("livraria", "livraria", "thalis", "10.61.49.160", "thalis").initialize()
        cls.alfavoritaliv_table = AlFavoritaLivTable(cls.connection)
        cls.cursor = cls.connection.cursor()
        # Verifica o search_path
        cls.cursor.execute("SHOW search_path;")
        print(f"Search path atual: {cls.cursor.fetchone()[0]}")

    def setUp(self):
        # Define valores de teste baseados nos dados reais das tabelas Aluno e Livro
        self.isbn_liv = "9781686923500"  # ISBN existente na tabela Livro
        self.matricula_al = "001"        # Matrícula existente na tabela Aluno
        self.isbn_liv_alt = "9781521859292"  # Outro ISBN para testes de update
        self.matricula_al_alt = "002"        # Outra matrícula para testes de update

    def tearDown(self):
        # Remove os dados fictícios criados em AlFavoritaLiv após cada teste
        self.cursor.execute("DELETE FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        self.cursor.execute("DELETE FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv_alt, self.matricula_al_alt))
        self.connection.commit()

    def test_create_alfavoritaliv(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        self.cursor.execute("SELECT 1 FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, f"Falha ao inserir AlFavoritaLiv com ISBN {self.isbn_liv} e Matricula {self.matricula_al}")

    def test_create_alfavoritaliv_conflict(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.cursor.execute("SELECT COUNT(*) FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1, "Registro duplicado foi inserido")

    def test_create_alfavoritaliv_invalid_isbn(self):
        invalid_isbn = "9999999999999"
        with self.assertRaises(ValueError, msg="Deveria falhar ao inserir ISBN inexistente"):
            self.alfavoritaliv_table.create(invalid_isbn, self.matricula_al)

    def test_create_alfavoritaliv_invalid_matricula(self):
        invalid_matricula = "999"
        with self.assertRaises(ValueError, msg="Deveria falhar ao inserir matrícula inexistente"):
            self.alfavoritaliv_table.create(self.isbn_liv, invalid_matricula)

    def test_read_alfavoritaliv(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        result = self.alfavoritaliv_table.read(qtd=10, pagina=1, filter={"ISBNLiv": self.isbn_liv, "MatriculaAl": self.matricula_al})
        print(f"Registros lidos no teste: {result['registros']}")
        self.assertEqual(len(result["registros"]), 1, "Filtro retornou número incorreto de registros")
        self.assertEqual(result["registros"][0][0], self.isbn_liv, "ISBN incorreto no registro filtrado")
        self.assertEqual(result["registros"][0][1], self.matricula_al, "Matrícula incorreta no registro filtrado")

    def test_read_alfavoritaliv_with_filter(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        result = self.alfavoritaliv_table.read(filter={"ISBNLiv": self.isbn_liv, "MatriculaAl": self.matricula_al})
        self.assertEqual(len(result["registros"]), 1, "Filtro retornou número incorreto de registros")
        self.assertEqual(result["registros"][0][0], self.isbn_liv, "ISBN incorreto no registro filtrado")
        self.assertEqual(result["registros"][0][1], self.matricula_al, "Matrícula incorreta no registro filtrado")

    def test_read_alfavoritaliv_invalid_filter(self):
        with self.assertRaises(ValueError, msg="Deveria falhar com filtro inválido"):
            self.alfavoritaliv_table.read(filter={"ColunaInvalida": "valor"})

    def test_read_invalid_qtd(self):
        result = self.alfavoritaliv_table.read(qtd=0)
        self.assertEqual(result, {}, "Leitura com qtd=0 não retornou dicionário vazio")

    def test_update_alfavoritaliv(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        self.alfavoritaliv_table.update(self.isbn_liv, self.matricula_al, self.isbn_liv_alt, self.matricula_al_alt)
        self.cursor.execute("SELECT 1 FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv_alt, self.matricula_al_alt))
        self.assertIsNotNone(self.cursor.fetchone(), "Falha ao atualizar para o novo registro")
        self.cursor.execute("SELECT 1 FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        self.assertIsNone(self.cursor.fetchone(), "Registro antigo ainda existe")

    def test_update_alfavoritaliv_nonexistent(self):
        non_existent_isbn = "9999999999999"
        non_existent_matricula = "999"
        self.alfavoritaliv_table.update(
            non_existent_isbn, non_existent_matricula,
            self.isbn_liv, self.matricula_al
        )
        self.cursor.execute("SELECT 1 FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        self.assertIsNone(self.cursor.fetchone(), "Registro inserido para atualização inexistente")

    def test_update_alfavoritaliv_invalid_new_isbn(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        invalid_isbn = "9999999999999"
        with self.assertRaises(ValueError, msg="Deveria falhar ao atualizar para ISBN inexistente"):
            self.alfavoritaliv_table.update(self.isbn_liv, self.matricula_al, invalid_isbn, self.matricula_al_alt)

    def test_update_alfavoritaliv_invalid_new_matricula(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        invalid_matricula = "999"
        with self.assertRaises(ValueError, msg="Deveria falhar ao atualizar para matrícula inexistente"):
            self.alfavoritaliv_table.update(self.isbn_liv, self.matricula_al, self.isbn_liv_alt, invalid_matricula)

    def test_delete_alfavoritaliv(self):
        self.alfavoritaliv_table.create(self.isbn_liv, self.matricula_al)
        self.connection.commit()
        self.alfavoritaliv_table.delete(self.isbn_liv, self.matricula_al)
        self.cursor.execute("SELECT 1 FROM AlFavoritaLiv WHERE ISBNLiv = %s AND MatriculaAl = %s;",
                           (self.isbn_liv, self.matricula_al))
        result = self.cursor.fetchone()
        self.assertIsNone(result, "Registro não foi removido")

    def test_delete_alfavoritaliv_nonexistent(self):
        non_existent_isbn = "9999999999999"
        non_existent_matricula = "999"
        self.alfavoritaliv_table.delete(non_existent_isbn, non_existent_matricula)

    @classmethod
    def tearDownClass(cls):
        if not cls.connection.closed:
            cls.cursor.close()
            cls.alfavoritaliv_table.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)