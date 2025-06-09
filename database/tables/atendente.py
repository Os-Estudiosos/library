from database import Connection
from database.tables import Table

class AtendenteTable:
    
    def __init__(self, connection:Connection):
        self.conn = connection
        self.values = "(CPFAtt, PrimeiroNomeAtt, UltimoNomeAtt)"
        self.name = "Atendente"

    def create(self, cpf_att, primeiro_nome_att, ultimo_nome_att):
        try:
            sql = f"""
            INSERT INTO {self.name} {self.values} VALUES (%s, %s, %s)
            ON CONFLICT (CPFAtt) DO UPDATE SET
            PrimeiroNomeAtt = EXCLUDED.PrimeiroNomeAtt,
            UltimoNomeAtt = EXCLUDED.UltimoNomeAtt;
            """
            self.conn.cursor().execute(sql, (cpf_att, primeiro_nome_att, ultimo_nome_att))
            self.conn.commit()
            print(f"{self.name} inserida com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir:", e)

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
        
    def update(self, cpf_att, primeiro_nome_att, ultimo_nome_att):
        try:
            sql = f"UPDATE {self.name} SET PrimeiroNomeAtt = %s, UltimoNomeAtt = %s WHERE CPFAtt = %s;"
            self.conn.cursor().execute(sql, (primeiro_nome_att, ultimo_nome_att, cpf_att))
            self.conn.commit()
            print(f"{self.name} atualizada com sucesso.")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar:", e)

    def delete(self, cpf_att):
        try:
            sql = f"DELETE FROM {self.name} WHERE CPFAtt = %s;"
            self.conn.cursor().execute(sql, (cpf_att,))
            if self.conn.cursor().rowcount == 0:
                print(f"{self.name} com CPF {cpf_att} não encontrada.")
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
