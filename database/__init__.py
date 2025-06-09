import psycopg2

class Connection:
    def __init__(self, db_name, path, owner, password, host):
        self.db_name = db_name
        self.path = path
        self.owner = owner
        self.password = password
        self.host = host
        self.cursor = None
        self.connection = None
    
    def __str__(self):
        print(f"O banco de dados {self.db_name} pertence a {self.owner} e tem o caminho {self.path}")
    
    # Conexão com o banco (PostgreSQL)
    def initialize(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.owner,
                password=self.password,
                host=self.host,
                port="5432"
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SET search_path TO {self.path};")
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
