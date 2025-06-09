from database import Connection

class SuspensaoTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(IdSusp, DataInicioSusp, DataFimSusp, MatriculaAl)"
        self.name = "Suspensao"

    def create(self, id_susp, data_inicio_susp, data_fim_susp, matricula_al):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s, %s, %s)
            ON CONFLICT (IdSusp, MatriculaAl) DO UPDATE SET
            DataInicioSusp = EXCLUDED.DataInicioSusp,
            DataFimSusp = EXCLUDED.DataFimSusp;
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_susp, data_inicio_susp, data_fim_susp, matricula_al))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
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

    def update(self, id_susp, data_inicio_susp, data_fim_susp, matricula_al):
        try:
            sql = f"UPDATE {self.name} SET DataInicioSusp = %s, DataFimSusp = %s WHERE IdSusp = %s AND MatriculaAl = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (data_inicio_susp, data_fim_susp, id_susp, matricula_al))
            if cursor.rowcount == 0:
                print(f"{self.name} com IdSusp {id_susp} e MatriculaAl {matricula_al} não encontrada.")
                return
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)
        finally:
            cursor.close()

    def delete(self, id_susp, matricula_al):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdSusp = %s AND MatriculaAl = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_susp, matricula_al))
            if cursor.rowcount == 0:
                print(f"{self.name} com IdSusp {id_susp} e MatriculaAl {matricula_al} não encontrada.")
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