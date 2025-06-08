from database import Connection
from database.tables import Table

class TurmaTable(Connection.initialize):
    
    def __init__(self, db_name, path, owner):
        super().__init__(db_name, path, owner)
        self.conn = self.initialize()
        self.values = "(IdTurma, NomeTurma)"
        self.name = "Turma"

    def create(self, id_turma, nome_turma):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (IdTurma) DO UPDATE SET
            NomeTurma = EXCLUDED.NomeTurma;
            """
            self.conn.cursor().execute(sql, (id_turma, nome_turma))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, filter=None):
        dict = {}
        try:
            total_registros = self.conn.cursor().execute(f"SELECT COUNT(*) FROM {self.name};").fetchone()[0]
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
            sql = f"SELECT {qtd} FROM {self.name}"
            if filter:
                sql += f" WHERE {[f'{k} = %s' for k in filter.keys()]}"
            sql += ";"            
            dict["pagina_atual"] = 1
            dict["registros"] = [self.conn.cursor().execute(sql, tuple(filter.values())).fetchall()]
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, id_turma, nome_turma):
        try:
            sql = f"UPDATE {self.name} SET NomeTurma = %s WHERE IdTurma = %s;"
            self.conn.cursor().execute(sql, (nome_turma, id_turma))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, id_turma):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdTurma = %s;"
            self.conn.cursor().execute(sql, (id_turma,))
            if self.conn.cursor().rowcount == 0:
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
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print("Erro ao fechar a conexão:", e)
        else:
            print("Nenhuma conexão para fechar.")
