from database import Connection

class CategoriaTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(IdCat, NomeCat)"
        self.name = "Categoria"

    def create(self, id_cat, nome_cat):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (IdCat) DO UPDATE SET
            NomeCat = EXCLUDED.NomeCat;
            """
            self.conn.cursor().execute(sql, (id_cat, nome_cat))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, filter=None, pagina=1):
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
            sql = f"SELECT * FROM {self.name}"
            params = []
            if filter:
                conditions = " AND ".join([f"{k} = %s" for k in filter.keys()])
                sql += f" WHERE {conditions}"
                params.extend(filter.values())
            sql += f" LIMIT %s OFFSET %s;"
            params.extend([qtd, offset])
            
            cursor.execute(sql, tuple(params))
            dict["registros"] = cursor.fetchall()
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, id_cat, nome_cat):
        try:
            sql = f"UPDATE {self.name} SET NomeCat = %s WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, (nome_cat, id_cat))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, id_cat):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdCat = %s;"
            self.conn.cursor().execute(sql, (id_cat,))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com ID {id_cat} não encontrada.")
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
