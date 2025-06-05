import psycopg2

class Connection:
    def __init__(self, db_name, path, owner):
        self.db_name = db_name
        self.path = path
        self.owner = owner
    
    def __str__(self):
        print(f"O banco de dados {self.db_name} pertence a {self.owner} e tem o caminho {self.path}")
    
    # Conexão com o banco (PostgreSQL)
    def initialize(self):
        try:
            conn = psycopg2.connect(dbname=self.db_name)
            # Define o schema default
            conn.cursor().execute(f"SET search_path TO {self.path};")
            conn.commit() # Adicionado para garantir que o search_path seja aplicado à sessão
            return conn
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None
