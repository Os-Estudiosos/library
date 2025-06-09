from database import Connection
from database.tables import Table

class LiPertenceCatTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(ISBNLiv, IdCat)"
        self.name = "LiPertenceCat"

    def create(self, isbn_liv, id_cat):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (ISBNLiv, IdCat) DO UPDATE SET
            IdCat = EXCLUDED.IdCat;
            """
            self.conn.cursor().execute(sql, (isbn_liv, id_cat))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, pagina=1, filter=None):
        dict = {}
        try:
            cursor = self.conn.cursor()
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
            sql = f"SELECT * FROM {self.name} LIMIT %s OFFSET %s"
            params = [qtd, offset]
            
            if filter:
                filter_conditions = " AND ".join([f"{k} = %s" for k in filter.keys()])
                sql = f"SELECT * FROM {self.name} WHERE {filter_conditions} LIMIT %s OFFSET %s"
                params = list(filter.values()) + [qtd, offset]
            
            cursor.execute(sql, tuple(params))
            dict["registros"] = cursor.fetchall()
            cursor.close()
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, isbn_liv, id_cat):
        try:
            sql = f"UPDATE {self.name} SET IdCat = %s WHERE ISBNLiv = %s;"
            self.conn.cursor().execute(sql, (id_cat, isbn_liv))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, isbn_liv, id_cat):
        try:
            sql = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
            self.conn.cursor().execute(sql, (isbn_liv, id_cat))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com ISBN {isbn_liv} e ID {id_cat} não encontrada.")
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
