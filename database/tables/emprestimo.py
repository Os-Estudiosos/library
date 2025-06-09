from database import Connection
from database.tables import Table

class EmprestimoTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(IdEmp, DataInicioEmp, DataFimEmp, BaixaEmp, MatriculaAl, ISBNLiv, CPFAtt)"
        self.name = "Emprestimo"

    def create(self, id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (IdEmp, MatriculaAl) DO UPDATE SET
            DataInicioEmp = EXCLUDED.DataInicioEmp,
            DataFimEmp = EXCLUDED.DataFimEmp,
            BaixaEmp = EXCLUDED.BaixaEmp,
            ISBNLiv = EXCLUDED.ISBNLiv,
            CPFAtt = EXCLUDED.CPFAtt;
            """
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att))
            self.conn.commit()
            print(f"{self.name} inserido com sucesso.")
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

    def update(self, id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att):
        try:
            sql = f"UPDATE {self.name} SET DataInicioEmp = %s, DataFimEmp = %s, BaixaEmp = %s, ISBNLiv = %s, CPFAtt = %s WHERE IdEmp = %s AND MatriculaAl = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (data_inicio_emp, data_fim_emp, baixa_emp, isbn_liv, cpf_att, id_emp, matricula_al))
            if cursor.rowcount == 0:
                print(f"{self.name} com IdEmp {id_emp} e MatriculaAl {matricula_al} não encontrado.")
                return
            self.conn.commit()
            print(f"{self.name} atualizado com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)
        finally:
            cursor.close()

    def delete(self, id_emp, matricula_al):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdEmp = %s AND MatriculaAl = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_emp, matricula_al))
            if cursor.rowcount == 0:
                print(f"{self.name} com IdEmp {id_emp} e MatriculaAl {matricula_al} não encontrado.")
                return
            self.conn.commit()
            print(f"{self.name} excluído com sucesso.")
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