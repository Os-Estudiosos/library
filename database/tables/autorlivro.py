from database import Connection
from database.tables import Table
import pandas as pd

class AutorLivroTable:
    
    def __init__(self, connection: Connection):
        if not connection or connection.closed:
            raise ValueError("Conexão inválida ou fechada.")
        self.conn = connection
        self.values = "(AutorLiv, ISBNLiv)"
        self.name = "AutorLivro"

    def create(self, autor_liv, isbn_liv):
        if not isinstance(isbn_liv, str) or len(isbn_liv) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        if not isinstance(autor_liv, str) or len(autor_liv.strip()) == 0:
            raise ValueError("Autor deve ser uma string não vazia.")
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s)
            ON CONFLICT (AutorLiv, ISBNLiv) DO NOTHING;
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, (autor_liv, isbn_liv))
            if cursor.rowcount > 0:
                self.conn.commit()
                print(f"{self.name} inserida com sucesso.")
            else:
                self.conn.rollback()
                print(f"{self.name} já existe com AutorLiv {autor_liv} e ISBNLiv {isbn_liv}.")
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

    def update(self, autor_liv_old, isbn_liv_old, autor_liv_new, isbn_liv_new):
        if not isinstance(isbn_liv_old, str) or len(isbn_liv_old) != 13:
            raise ValueError("ISBN antigo deve ser uma string de 13 caracteres.")
        if not isinstance(isbn_liv_new, str) or len(isbn_liv_new) != 13:
            raise ValueError("ISBN novo deve ser uma string de 13 caracteres.")
        if not isinstance(autor_liv_old, str) or len(autor_liv_old.strip()) == 0:
            raise ValueError("Autor antigo deve ser uma string não vazia.")
        if not isinstance(autor_liv_new, str) or len(autor_liv_new.strip()) == 0:
            raise ValueError("Autor novo deve ser uma string não vazia.")
        try:
            cursor = self.conn.cursor()
            sql_check = f"SELECT 1 FROM {self.name} WHERE AutorLiv = %s AND ISBNLiv = %s;"
            cursor.execute(sql_check, (autor_liv_old, isbn_liv_old))
            if cursor.rowcount == 0:
                print(f"{self.name} com AutorLiv {autor_liv_old} e ISBNLiv {isbn_liv_old} não encontrada.")
                return
            
            # Verifica se o novo registro já existe
            sql_check_new = f"SELECT 1 FROM {self.name} WHERE AutorLiv = %s AND ISBNLiv = %s;"
            cursor.execute(sql_check_new, (autor_liv_new, isbn_liv_new))
            if cursor.rowcount > 0:
                print(f"{self.name} com AutorLiv {autor_liv_new} e ISBNLiv {isbn_liv_new} já existe.")
                # Exclui o registro antigo, já que o novo já existe
                sql_delete = f"DELETE FROM {self.name} WHERE AutorLiv = %s AND ISBNLiv = %s;"
                cursor.execute(sql_delete, (autor_liv_old, isbn_liv_old))
                self.conn.commit()
                print(f"{self.name} atualizada com sucesso: AutorLiv {autor_liv_old} removido, pois {autor_liv_new} já existe.")
                return
            sql_delete = f"DELETE FROM {self.name} WHERE AutorLiv = %s AND ISBNLiv = %s;"
            cursor.execute(sql_delete, (autor_liv_old, isbn_liv_old))
            sql_insert = f"INSERT INTO {self.name} {self.values} VALUES (%s, %s);"
            cursor.execute(sql_insert, (autor_liv_new, isbn_liv_new))
            
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso: ({autor_liv_old}, {isbn_liv_old}) para ({autor_liv_new}, {isbn_liv_new}).")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)
        finally:
            cursor.close()

    def delete(self, autor_liv, isbn_liv):
        if not isinstance(isbn_liv, str) or len(isbn_liv) != 13:
            raise ValueError("ISBN deve ser uma string de 13 caracteres.")
        if not isinstance(autor_liv, str) or len(autor_liv.strip()) == 0:
            raise ValueError("Autor deve ser uma string não vazia.")
        try:
            sql = f"DELETE FROM {self.name} WHERE AutorLiv = %s AND ISBNLiv = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (autor_liv, isbn_liv))
            if cursor.rowcount == 0:
                print(f"{self.name} com AutorLiv {autor_liv} e ISBNLiv {isbn_liv} não encontrada.")
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
                self.name = "AutorLivro"

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
                SELECT AutorLivro.AutorLiv,
                AutorLivro.ISBNLiv
                {base_sql}
            """
            params = []
            if filter:
                sql += f" WHERE {where_clause}"
                params.extend(filter.values())
            sql += " ORDER BY AutorLivro.AutorLiv LIMIT %s OFFSET %s"
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
                    "Nome Autor", "ISBN Livro"
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
