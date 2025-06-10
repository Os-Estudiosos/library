from database import Connection
import pandas as pd
from database.tables import Table

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
            
    def __init__(self, connection: Connection):
        self.conn = connection
        self.name = "Suspensao"

    def create(self, primary_key: dict, colums: dict):
        try:
            all_columns = list(primary_key.keys()) + list(colums.keys())
            all_values = list(primary_key.values()) + list(colums.values())
            col_names = ', '.join(all_columns)
            placeholders = ', '.join(['%s'] * len(all_columns))
            conflict_key = ', '.join(primary_key.keys())
            update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in colums.keys()])
            sql = f"""
            INSERT INTO {self.name} ({col_names})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_key}) DO UPDATE SET
            {update_set};
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, all_values)
            self.conn.commit()
            cursor.close()
            print(f"{self.name} inserida ou atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, filter: dict = None, qtd=15, pagina=1):
        resultado = {}
        cursor = None
        try:
            cursor = self.conn.cursor()
            base_sql = f"""
                FROM {self.name}
            """
            if filter:
                where_clause = " AND ".join([f"{k} = %s" for k in filter.keys()])
                count_sql = f"SELECT COUNT(*) {base_sql} WHERE {where_clause};"
                cursor.execute(count_sql, list(filter.values()))
            else:
                count_sql = f"SELECT COUNT(*) {base_sql};"
                cursor.execute(count_sql)
            total_registros = cursor.fetchone()[0]
            if total_registros == 0:
                print("Nenhum registro encontrado.")
                return {}
            registros_por_pagina = min(qtd, total_registros)
            total_paginas = (total_registros + registros_por_pagina - 1) // registros_por_pagina
            offset = (pagina - 1) * registros_por_pagina
            sql = f"""
                SELECT CPFAtt,
                       CONCAT(PrimeiroNomeAtt, ' ', UltimoNomeAtt) AS NomeCompleto
                {base_sql}
            """
            params = []
            if filter:
                sql += f" WHERE {where_clause}"
                params.extend(filter.values())
            sql += " ORDER BY CPFAtt LIMIT %s OFFSET %s"
            params.extend([registros_por_pagina, offset])
            cursor.execute(sql, tuple(params))
            registros = cursor.fetchall()
            cursor.close()
            resultado.update({
                "total_registros": total_registros,
                "registros_por_pagina": registros_por_pagina,
                "total_paginas": total_paginas,
                "pagina_atual": pagina,
                "registros": pd.DataFrame(registros, columns=[
                    "CPF", "Nome completo"
                ])
            })
            return resultado
        except Exception as e:
            print("Erro ao ler:", e)
            if cursor:
                cursor.close()
            return {}

    def update(self, primary_key: dict, colums: dict):
        try:
            if not primary_key or not colums:
                print("Chave primária e colunas a atualizar não podem estar vazias.")
                return
            set_clause = ', '.join([f"{col} = %s" for col in colums.keys()])
            where_clause = ' AND '.join([f"{pk} = %s" for pk in primary_key.keys()])
            values = list(colums.values()) + list(primary_key.values())
            sql = f"""
            UPDATE {self.name}
            SET {set_clause}
            WHERE {where_clause};
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, values)
            self.conn.commit()
            cursor.close()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, primary_key: dict):
        try:
            if not primary_key:
                print("Chave primária não pode estar vazia.")
                return
            where_clause = ' AND '.join([f"{pk} = %s" for pk in primary_key.keys()])
            values = list(primary_key.values())
            sql = f"DELETE FROM {self.name} WHERE {where_clause};"
            cursor = self.conn.cursor()
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                print(f"{self.name} com os critérios {primary_key} não encontrada.")
                cursor.close()
                return
            self.conn.commit()
            cursor.close()
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