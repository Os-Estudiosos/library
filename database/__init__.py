import psycopg2

class Connection:
    def __init__(self, db_name, path, user, host, password):
        self.db_name = db_name
        self.path = path
        self.user = user
        self.host = host
        self.password = password
    
    def __str__(self):
        return f"O banco de dados {self.db_name} está sendo usado por {self.user} e tem o caminho {self.path}"
  
    def initialize(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,  
                host=self.host,
                port="5432"
            )

            conn.cursor().execute(f"SET search_path TO {self.path};")
            conn.commit() 
            return conn
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None