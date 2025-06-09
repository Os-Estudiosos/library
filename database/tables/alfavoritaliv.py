from database import Connection

class AlFavoritaLivTable:
    
    def __init__(self, connection: Connection):
        if not connection or connection.closed:
            raise ValueError("Conexão inválida ou fechada.")
        self.conn = connection
        self.values = "(ISBNLiv, MatriculaAl)"
        self.name = "AlFavoritaLiv"
        self.valid_columns = {"ISBNLiv", "MatriculaAl"}

    def _check_isbn_exists(self, isbn_liv):
        """Verifica se o ISBN existe na tabela Livro."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Livro WHERE ISBNLiv = %s;", (isbn_liv,))
            return cursor.fetchone() is not None

    def _check_matricula_exists(self, matricula_al):
        """Verifica se a MatriculaAl existe na tabela Aluno."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Aluno WHERE MatriculaAl = %s;", (matricula_al,))
            return cursor.fetchone() is not None

    def create(self, isbn_liv, matricula_al):
        if not isinstance(isbn_liv, str) or len(isbn_liv) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        if not self._check_isbn_exists(isbn_liv):
            raise ValueError(f"ISBN {isbn_liv} não encontrado na tabela Livro.")
        if not self._check_matricula_exists(matricula_al):
            raise ValueError(f"Matrícula {matricula_al} não encontrada na tabela Aluno.")
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (ISBNLiv, MatriculaAl) DO NOTHING;
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (isbn_liv, matricula_al))
                if cursor.rowcount > 0:
                    self.conn.commit()
                    print(f"{self.name} inserida com sucesso.")
                else:
                    self.conn.rollback()
                    print(f"{self.name} já existe com ISBNLiv {isbn_liv} e MatriculaAl {matricula_al}.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir ({isbn_liv}, {matricula_al}): {e}")

    def read(self, qtd=15, pagina=1, filter=None):
        dict = {}
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {self.name};")
                total_registros = cursor.fetchone()[0]
                
                if qtd <= 0:
                    print("Quantidade de registros por página deve ser maior que zero.")
                    return {}
                if qtd > total_registros:
                    qtd = total_registros
                
                registros_por_pagina = qtd
                total_paginas = (total_registros + registros_por_pagina - 1) // registros_por_pagina
                dict["total_registros"] = total_registros
                dict["registros_por_pagina"] = registros_por_pagina
                dict["total_paginas"] = total_paginas
                dict["pagina_atual"] = pagina
                
                offset = (pagina - 1) * qtd
                sql = f"SELECT * FROM {self.name}"
                params = []
                if filter:
                    print(f"Filtro recebido: {filter}")  # Log para depuração
                    invalid_columns = [k for k in filter.keys() if k not in self.valid_columns]
                    if invalid_columns:
                        raise ValueError(f"Filtro contém colunas inválidas: {invalid_columns}")
                    filter_conditions = " AND ".join([f"{k} = %s" for k in filter.keys()])
                    sql += f" WHERE {filter_conditions}"
                    params.extend(filter.values())
                sql += f" ORDER BY ISBNLiv, MatriculaAl LIMIT %s OFFSET %s"
                params.extend([qtd, offset])
                
                cursor.execute(sql, tuple(params))
                dict["registros"] = cursor.fetchall()
                print(f"Registros retornados: {dict['registros']}")  # Log para depuração
                return dict
        except ValueError as e:
            print(f"Erro ao ler registros: {e}")
            raise  # Propaga ValueError para filtros inválidos
        except Exception as e:
            print(f"Erro ao ler registros: {e}")
            return {}

    def update(self, isbn_liv_old, matricula_al_old, isbn_liv_new, matricula_al_new):
        if not isinstance(isbn_liv_old, str) or len(isbn_liv_old) != 13:
            raise ValueError("ISBN antigo deve ser uma string de 13 caracteres.")
        if not isinstance(isbn_liv_new, str) or len(isbn_liv_new) != 13:
            raise ValueError("ISBN novo deve ser uma string de 13 caracteres.")
        if not self._check_isbn_exists(isbn_liv_new):
            raise ValueError(f"ISBN novo {isbn_liv_new} não encontrado na tabela Livro.")
        if not self._check_matricula_exists(matricula_al_new):
            raise ValueError(f"Matrícula nova {matricula_al_new} não encontrada na tabela Aluno.")
        try:
            with self.conn.cursor() as cursor:
                # Verifica se o registro antigo existe
                sql_check = f"SELECT 1 FROM {self.name} WHERE ISBNLiv = %s AND MatriculaAl = %s;"
                cursor.execute(sql_check, (isbn_liv_old, matricula_al_old))
                if cursor.rowcount == 0:
                    print(f"{self.name} com ISBNLiv {isbn_liv_old} e MatriculaAl {matricula_al_old} não encontrada.")
                    return
                
                # Verifica se a nova combinação já existe
                sql_check_new = f"SELECT 1 FROM {self.name} WHERE ISBNLiv = %s AND MatriculaAl = %s;"
                cursor.execute(sql_check_new, (isbn_liv_new, matricula_al_new))
                if cursor.fetchone():
                    self.conn.rollback()
                    print(f"{self.name} com ISBNLiv {isbn_liv_new} e MatriculaAl {matricula_al_new} já existe.")
                    return
                
                # Exclui a relação antiga
                sql_delete = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND MatriculaAl = %s;"
                cursor.execute(sql_delete, (isbn_liv_old, matricula_al_old))
                
                # Insere a nova relação
                sql_insert = f"INSERT INTO {self.name} {self.values} VALUES (%s, %s);"
                cursor.execute(sql_insert, (isbn_liv_new, matricula_al_new))
                
                self.conn.commit()
                print(f"{self.name} atualizada com sucesso: ({isbn_liv_old}, {matricula_al_old}) para ({isbn_liv_new}, {matricula_al_new}).")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar ({isbn_liv_old}, {matricula_al_old}) para ({isbn_liv_new}, {matricula_al_new}): {e}")

    def delete(self, isbn_liv, matricula_al):
        if not isinstance(isbn_liv, str) or len(isbn_liv) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        try:
            with self.conn.cursor() as cursor:
                sql = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND MatriculaAl = %s;"
                cursor.execute(sql, (isbn_liv, matricula_al))
                if cursor.rowcount == 0:
                    print(f"{self.name} com ISBNLiv {isbn_liv} e MatriculaAl {matricula_al} não encontrada.")
                    return
                self.conn.commit()
                print(f"{self.name} excluída com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir ({isbn_liv}, {matricula_al}): {e}")

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print(f"Erro ao fechar a conexão: {e}")
        else:
            print("Nenhuma conexão para fechar.")