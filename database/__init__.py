import psycopg2

class Connection:
    def __init__(self, db_name, path, user, host, password):
        self.db_name = db_name
        self.path = path
        self.user = user
        self.host = host
        self.password = password
        self.conn = None
    
    def initialize(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,  
                host=self.host,
                port="5432"
            )
            self.conn.cursor().execute(f"SET search_path TO {self.path};")
            self.conn.commit() 
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            self.conn = None
    
    def cursor(self):
        return self.conn.cursor() if self.conn else None

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()
