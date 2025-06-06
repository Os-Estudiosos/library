from database import Connection
from database.tables import Table

class CategoriaTable(Connection.initialize):
    def __init__(self, db_name, path, owner):
        super().__init__(db_name, path, owner)
        self.conn = self.initialize()
        self.values = "(IdCat, NomeCat)"

    def create(self, *values):
        try:
            sql = f"""
            INSERT INTO Categoria {self.values} VALUES (%s, %s)
            ON CONFLICT (IdCat) DO UPDATE SET
            NomeCat = EXCLUDED.NomeCat;
            """
            self.conn.cursor().execute(sql, *values)
            self.conn.commit()
            print("Categoria inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd="*", filter=None):
        try:
            sql = f"SELECT {qtd} FROM Categoria"
            if filter:
                sql += f" WHERE {filter}"
            sql += ";"
            return self.conn.cursor().execute(sql).fetchall()
        except Exception as e:
            print("Erro ao ler:", e)
            return []

    def update(self, *values):
        try:
            sql = f"UPDATE Categoria SET NomeCat = %s WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, values)
            self.conn.commit()
            print("Categoria atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, *values):
        try:
            sql = f"DELETE FROM Categoria WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, values)
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
