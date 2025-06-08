from database import Connection
from database.tables import Table

class EmprestimoTable(Connection.initialize):
    
    def __init__(self, db_name, path, owner):
        super().__init__(db_name, path, owner)
        self.conn = self.initialize()
        self.values = "(IdEmp, DataInicioEmp, DataFimEmp, BaixaEmp, MatriculaAl, ISBNLiv, CPFAtt)"
        self.name = "Emprestimo"

    def create(self, id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (IdEmp) DO UPDATE SET
            DataInicioEmp = EXCLUDED.DataInicioEmp,
            DataFimEmp = EXCLUDED.DataFimEmp,
            BaixaEmp = EXCLUDED.BaixaEmp,
            MatriculaAl = EXCLUDED.MatriculaAl,
            ISBNLiv = EXCLUDED.ISBNLiv,
            CPFAtt = EXCLUDED.CPFAtt;
            """
            self.conn.cursor().execute(sql, (id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

    def read(self, qtd=15, filter=None):
        dict = {}
        try:
            total_registros = self.conn.cursor().execute(f"SELECT COUNT(*) FROM {self.name};").fetchone()[0]
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
            sql = f"SELECT {qtd} FROM {self.name}"
            if filter:
                sql += f" WHERE {[f'{k} = %s' for k in filter.keys()]}"
            sql += ";"            
            dict["pagina_atual"] = 1
            dict["registros"] = [self.conn.cursor().execute(sql, tuple(filter.values())).fetchall()]
            return dict
        except Exception as e:
            print("Erro ao ler:", e)
            return {}

    def update(self, id_emp, data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att):
        try:
            sql = f"UPDATE {self.name} SET DataInicioEmp = %s, DataFimEmp = %s, BaixaEmp = %s, MatriculaAl = %s, ISBNLiv = %s, CPFAtt = %s WHERE IdEmp = %s;"
            self.conn.cursor().execute(sql, (data_inicio_emp, data_fim_emp, baixa_emp, matricula_al, isbn_liv, cpf_att, id_emp))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, id_emp):
        try:
            sql = f"DELETE FROM {self.name} WHERE IdEmp = %s;"
            self.conn.cursor().execute(sql, (id_emp,))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com ID {id_emp} não encontrada.")
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
