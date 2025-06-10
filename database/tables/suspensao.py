from database import Connection
import pandas as pd
from database.tables import Table

class SuspensaoTable:
            
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
                INNER JOIN Aluno ON Suspensao.MatriculaAl = Aluno.MatriculaAl
            """
            if filter:
                where_clause = " AND ".join([f"Suspensao.{k} = %s" for k in filter.keys()])
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
                SELECT Suspensao.IdSusp,
                    Suspensao.DataInicioSusp,
                    Suspensao.DataFimSusp,
                    CONCAT(Aluno.PrimeiroNomeAl, ' ', Aluno.UltimoNomeAl) AS NomeCompleto
                {base_sql}
            """
            params = []
            if filter:
                sql += f" WHERE {where_clause}"
                params.extend(filter.values())
            sql += " ORDER BY Suspensao.DataInicioSusp LIMIT %s OFFSET %s"
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
                    "Id Suspensão", "Data Início", "Data Fim", "Nome Aluno"
                ]),
                "bruto": pd.DataFrame(
                    registros,
                    columns=["idsusp", "datainiciosusp", "datafimsusp", "matriculaal"],
                )
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