from database import Connection

class AlFavoritaLivTable:
    def __init__(self, connection: Connection):
        if not connection or connection.closed:
            raise ValueError("Conexão inválida ou fechada.")
        self.conn = connection
        self.values = "(ISBNLiv, MatriculaAl)"
        self.name = "AlFavoritaLiv"

    def create(self, isbn_liv, matricula_al):
        if not isinstance(isbn_liv, str) or len(isbn_liv) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        try:
            sql = """
            INSERT INTO {} {} VALUES (%s, %s)
            ON CONFLICT (ISBNLiv, MatriculaAl) DO UPDATE SET MatriculaAl = EXCLUDED.MatriculaAl;
            """.format(self.name, self.values)
            self.conn.cursor().execute(sql, (isbn_liv, matricula_al))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, filter=None):
        dict_result = {}
        try:
            cursor = self.conn.cursor()
            total_registros = cursor.execute(f"SELECT COUNT(*) FROM {self.name};").fetchone()[0]
            if qtd <= 0:
                print("Quantidade de registros por página deve ser maior que zero.")
                return {}
            if qtd > total_registros:
                qtd = total_registros
            registros_por_pagina = qtd
            total_paginas = (total_registros + registros_por_pagina - 1) // registros_por_pagina
            dict_result["total_registros"] = total_registros
            dict_result["registros_por_pagina"] = registros_por_pagina
            dict_result["total_paginas"] = total_paginas
            sql = f"SELECT * FROM {self.name}"
            params = []
            if filter:
                conditions = " AND ".join([f"{k} = %s" for k in filter.keys()])
                sql += f" WHERE {conditions}"
                params.extend(filter.values())
            sql += " LIMIT %s"
            params.append(qtd)
            dict_result["pagina_atual"] = 1
            dict_result["registros"] = cursor.execute(sql, tuple(params)).fetchall()
            return dict_result
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, isbn, matricula_al):
        if not isinstance(isbn, str) or len(isbn) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        try:
            sql = f"UPDATE {self.name} SET MatriculaAl = %s WHERE ISBNLiv = %s;"
            self.conn.cursor().execute(sql, (matricula_al, isbn))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, isbn, matricula_al):
        if not isinstance(isbn, str) or len(isbn) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        try:
            sql = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND MatriculaAl = %s;"
            self.conn.cursor().execute(sql, (isbn, matricula_al))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com ISBN {isbn} e Matrícula {matricula_al} não encontrada.")
                return
            self.conn.commit()
            print(f"{self.name} excluída com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao excluir:", e)

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print("Erro ao fechar a conexão:", e)
        else:
            print("Nenhuma conexão para fechar.")