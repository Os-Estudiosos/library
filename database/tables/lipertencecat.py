from database import Connection
from database.tables import Table
import pandas as pd

class LiPertenceCatTable:

    def __init__(self, connection: Connection):
        self.conn = connection
        self.name = "LiPertenceCat"

    def create(self, primary_key: dict, colums: dict):
        try:
            all_columns = list(primary_key.keys()) + list(colums.keys())
            all_values = list(primary_key.values()) + list(colums.values())
            col_names = ', '.join(all_columns)
            placeholders = ', '.join(['%s'] * len(all_columns))
            conflict_key = ', '.join(primary_key.keys())
            
            if colums:
                update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in colums.keys()])
                sql = f"""
                INSERT INTO {self.name} ({col_names})
                VALUES ({placeholders})
                ON CONFLICT ({conflict_key}) DO UPDATE SET
                {update_set};
                """
            else:
                sql = f"""
                INSERT INTO {self.name} ({col_names})
                VALUES ({placeholders})
                ON CONFLICT ({conflict_key}) DO NOTHING;
                """
            
            with self.conn.cursor() as cursor:
                cursor.execute(sql, all_values)
                self.conn.commit()
                print(f"{self.name} inserida ou atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir. SQL: {sql} Valores: {all_values} Erro: {e}")

    def read(self, filter: dict = None, qtd=15, pagina=1):
        resultado = {}
        try:
            with self.conn.cursor() as cursor:
                base_sql = f"FROM {self.name}"
                if filter:
                    where_clause = " AND ".join([f"LiPertenceCat.{k} = %s" for k in filter.keys()])
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
                    SELECT LiPertenceCat.ISBNLiv, LiPertenceCat.IdCat
                    {base_sql}
                """
                params = []
                if filter:
                    sql += f" WHERE {where_clause}"
                    params.extend(filter.values())
                sql += " ORDER BY LiPertenceCat.IdCat LIMIT %s OFFSET %s"
                params.extend([registros_por_pagina, offset])
                cursor.execute(sql, tuple(params))
                registros = cursor.fetchall()
                
                resultado.update({
                    "total_registros": total_registros,
                    "registros_por_pagina": registros_por_pagina,
                    "total_paginas": total_paginas,
                    "pagina_atual": pagina,
                    "registros": pd.DataFrame(registros, columns=["ISBN Livro","ID Categoria"])
                })
                return resultado
        except Exception as e:
            print(f"Erro ao ler. SQL: {sql if 'sql' in locals() else ''} Erro: {e}")
            return {}

    def update(self, primary_key: dict, colums: dict):
        try:
            if not primary_key or not colums:
                raise ValueError("Chave primária e colunas a atualizar não podem estar vazias.")
            
            set_clause = ', '.join([f"{col} = %s" for col in colums.keys()])
            where_clause = ' AND '.join([f"{pk} = %s" for pk in primary_key.keys()])
            values = list(colums.values()) + list(primary_key.values())
            
            sql = f"""
            UPDATE {self.name}
            SET {set_clause}
            WHERE {where_clause};
            """
            
            with self.conn.cursor() as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar. SQL: {sql if 'sql' in locals() else ''} Erro: {e}")

    def delete(self, primary_key: dict):
        try:
            if not primary_key:
                raise ValueError("Chave primária não pode estar vazia.")
            
            where_clause = ' AND '.join([f"{pk} = %s" for pk in primary_key.keys()])
            values = list(primary_key.values())
            sql = f"DELETE FROM {self.name} WHERE {where_clause};"
            
            with self.conn.cursor() as cursor:
                cursor.execute(sql, values)
                if cursor.rowcount == 0:
                    print(f"{self.name} com os critérios {primary_key} não encontrada.")
                    return
                self.conn.commit()
                print(f"{self.name} excluída com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir. SQL: {sql if 'sql' in locals() else ''} Erro: {e}")

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print("Conexão fechada com sucesso.")
            except Exception as e:
                print("Erro ao fechar a conexão:", e)
        else:
            print("Nenhuma conexão para fechar.")
