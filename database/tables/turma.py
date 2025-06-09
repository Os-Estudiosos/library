from database import Connection

class TurmaTable:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.values = "(IdTurma, NomeTurma)"
        self.name = "Turma"
        self.cursor = self.conn.cursor()  # Reutilizar o cursor para eficiência

    def create(self, id_turma, nome_turma):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (IdTurma) DO UPDATE SET
            NomeTurma = EXCLUDED.NomeTurma;
            """
            self.cursor.execute(sql, (id_turma, nome_turma))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, pagina=1, filter=None):
        dict = {}
        try:
            # Calcular total de registros
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.name};")
            total_registros = self.cursor.fetchone()[0]
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

            # Construir a query SQL com LIMIT e OFFSET
            offset = (pagina - 1) * qtd
            sql = f"SELECT * FROM {self.name} LIMIT %s OFFSET %s"
            params = (qtd, offset)

            if filter:
                conditions = " AND ".join([f"{k} = %s" for k in filter.keys()])
                sql = f"SELECT * FROM {self.name} WHERE {conditions} LIMIT %s OFFSET %s"
                params = tuple(filter.values()) + (qtd, offset)

            self.cursor.execute(sql, params)
            dict["registros"] = self.cursor.fetchall()
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, id_turma, nome_turma):
        try:
            sql = f"UPDATE {self.name} SET NomeTurma = %s WHERE IdTurma = %s;"
            self.cursor.execute(sql, (nome_turma, id_turma))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, id_turma):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdTurma = %s;"
            self.cursor.execute(sql, (id_turma,))
            if self.cursor.rowcount == 0:
                print(f"{self.name} com ID {id_turma} não encontrada.")
                return
            self.conn.commit()
            print(f"{self.name} excluída com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao excluir:", e)

    def close(self):
        if self.conn:
            try:
                self.cursor.close()
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print("Erro ao fechar a conexão:", e)
        else:
            print("Nenhuma conexão para fechar.")