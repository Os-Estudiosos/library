from database import Connection
from config.database import *

from database.tables.atendente import AtendenteTable
from database.tables.aluno import AlunoTable
from database.tables.livro import LivroTable
from database.tables.suspensao import SuspensaoTable
from database.tables.turma import TurmaTable

connection = Connection(
    db_name=DB_NAME,
    host=DB_HOST,
    path=DB_PATH,
    password=DB_PASSWORD,
    user=DB_OWNER,
)
connection.initialize()

class TablesManager:
    connection=connection

    atendenteTable = AtendenteTable(connection)
    alunoTable = AlunoTable(connection)
    livroTable = LivroTable(connection)
    suspensaoTable = SuspensaoTable(connection)
    turmaTable = TurmaTable(connection)
