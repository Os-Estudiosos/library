from database import Connection
from database.tables import Table

class CategoriaTable(Connection.initialize):
    
    def __init__(self, db_name, path, owner):
        super().__init__(db_name, path, owner)
        self.conn = self.initialize()
        self.values = "(IdCat, NomeCat)"

    def create(self, id_cat, nome_cat):
        try:
            sql = f"""
            INSERT INTO Categoria {self.values} VALUES (%s, %s)
            ON CONFLICT (IdCat) DO UPDATE SET
            NomeCat = EXCLUDED.NomeCat;
            """
            self.conn.cursor().execute(sql, (id_cat, nome_cat))
            self.conn.commit()
            print("Categoria inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

# TODO: Filtro
    def read(self, qtd=15, filter=None):
        dict = {}
        try:
            total_registros = self.conn.cursor().execute("SELECT COUNT(*) FROM Categoria;").fetchone()[0]
            registros_por_pagina = qtd
            total_paginas = (total_registros + registros_por_pagina - 1) // registros_por_pagina
            dict["total_registros"] = total_registros
            dict["registros_por_pagina"] = registros_por_pagina
            dict["total_paginas"] = total_paginas
            sql = f"SELECT {qtd} FROM Categoria"
            if filter:
                sql += f" WHERE {filter}"
            sql += ";"            
            dict["pagina_atual"] = 1
            dict["registros"] = [self.conn.cursor().execute(sql).fetchall()]
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, id_cat, nome_cat):
        try:
            sql = f"UPDATE Categoria SET NomeCat = %s WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, (nome_cat, id_cat))
            self.conn.commit()
            print("Categoria atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, id_cat):
        try:
            sql = f"DELETE FROM Categoria WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, (id_cat,))
            if self.conn.cursor().rowcount == 0:
                print(f"Categoria com ID {id_cat} não encontrada.")
                return
            self.conn.commit()
            print("Categoria excluída com sucesso.")
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
