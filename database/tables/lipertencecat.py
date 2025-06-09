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
            ON CONFLICT (ISBNLiv, IdCat) DO NOTHING;
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, (isbn_liv, id_cat))
            if cursor.rowcount > 0:
                self.conn.commit()
                print(f"{self.name} inserida com sucesso.")
            else:
                self.conn.rollback()
                print(f"{self.name} já existe com ISBNLiv {isbn_liv} e IdCat {id_cat}.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)
        finally:
            cursor.close()

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

    def update(self, isbn_liv, id_cat_old, id_cat_new):
        try:
            cursor = self.conn.cursor()
            # Verifica se o registro antigo existe
            sql_check_old = f"SELECT 1 FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
            cursor.execute(sql_check_old, (isbn_liv, id_cat_old))
            if cursor.rowcount == 0:
                print(f"{self.name} com ISBNLiv {isbn_liv} e IdCat {id_cat_old} não encontrada.")
                return
            
            # Verifica se o novo registro já existe
            sql_check_new = f"SELECT 1 FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
            cursor.execute(sql_check_new, (isbn_liv, id_cat_new))
            if cursor.rowcount > 0:
                print(f"{self.name} com ISBNLiv {isbn_liv} e IdCat {id_cat_new} já existe.")
                # Exclui o registro antigo, já que o novo já existe
                sql_delete = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
                cursor.execute(sql_delete, (isbn_liv, id_cat_old))
                self.conn.commit()
                print(f"{self.name} atualizada com sucesso: IdCat {id_cat_old} removido, pois IdCat {id_cat_new} já existe.")
                return
            
            # Exclui a relação antiga
            sql_delete = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
            cursor.execute(sql_delete, (isbn_liv, id_cat_old))
            
            # Insere a nova relação
            sql_insert = f"INSERT INTO {self.name} {self.values} VALUES (%s, %s);"
            cursor.execute(sql_insert, (isbn_liv, id_cat_new))
            
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso: IdCat alterado de {id_cat_old} para {id_cat_new}.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)
        finally:
            cursor.close()

    def delete(self, isbn_liv, id_cat):
        try:
            sql = f"DELETE FROM {self.name} WHERE ISBNLiv = %s AND IdCat = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (isbn_liv, id_cat))
            if cursor.rowcount == 0:
                print(f"{self.name} com ISBNLiv {isbn_liv} e IdCat {id_cat} não encontrada.")
                return
            self.conn.commit()
            print(f"{self.name} excluída com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao excluir:", e)
        finally:
            cursor.close()

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print("Erro ao fechar a conexão:", e)
        else:
            print("Nenhuma conexão para fechar.")