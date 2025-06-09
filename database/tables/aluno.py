from database import Connection
from database.tables import Table

class AlunoTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(MatriculaAl, PrimeiroNomeAl, UltimoNomeAl, DataNascimentoAl, SenhaAl, IdTurma)"
        self.name = "Aluno"

    def create(self, matricula_al, primeiro_nome_al, ultimo_nome_al, data_nascimento_al, senha_al, id_turma):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (MatriculaAl) DO UPDATE SET
            PrimeiroNomeAl = EXCLUDED.PrimeiroNomeAl,
            UltimoNomeAl = EXCLUDED.UltimoNomeAl,
            DataNascimentoAl = EXCLUDED.DataNascimentoAl,
            SenhaAl = EXCLUDED.SenhaAl,
            IdTurma = EXCLUDED.IdTurma;
            """
            self.conn.cursor().execute(sql, (matricula_al, primeiro_nome_al, ultimo_nome_al, data_nascimento_al, senha_al, id_turma))
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

    def update(self, matricula_al, primeiro_nome_al, ultimo_nome_al, data_nascimento_al, senha_al, id_turma):
        try:
            sql = f"UPDATE {self.name} SET PrimeiroNomeAl = %s, UltimoNomeAl = %s, DataNascimentoAl = %s, SenhaAl = %s, IdTurma = %s WHERE MatriculaAl = %s;"
            self.conn.cursor().execute(sql, (primeiro_nome_al, ultimo_nome_al, data_nascimento_al, senha_al, id_turma, matricula_al))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, matricula_al):
        try:
            sql = f"DELETE FROM {self.name} WHERE MatriculaAl = %s;"
            self.conn.cursor().execute(sql, (matricula_al,))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com matrícula {matricula_al} não encontrada.")
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
