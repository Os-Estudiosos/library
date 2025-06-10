from database import Connection
from config.database import *

from database.tables.atendente import AtendenteTable
from database.tables.aluno import AlunoTable
from database.tables.livro import LivroTable
from database.tables.suspensao import SuspensaoTable
from database.tables.turma import TurmaTable
from database.tables.reserva import ReservaTable
from database.tables.grupo import GrupoTable
from database.tables.emprestimo import EmprestimoTable
from database.tables.categoria import CategoriaTable
from database.tables.lipertencecat import LiPertenceCatTable
from database.tables.autorlivro import AutorLivroTable
from database.tables.alfavoritaliv import AlFavoritaLivTable

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
    
    categoriaTable = CategoriaTable(connection)
    emprestimoTable = EmprestimoTable(connection)
    grupoTable = GrupoTable(connection)
    reservaTable = ReservaTable(connection)
    atendenteTable = AtendenteTable(connection)
    alunoTable = AlunoTable(connection)
    livroTable = LivroTable(connection)
    suspensaoTable = SuspensaoTable(connection)
    turmaTable = TurmaTable(connection)

    lipertencecatTable = LiPertenceCatTable(connection)
    autorlivroTable = AutorLivroTable(connection)
    alfavoritalivTable = AlFavoritaLivTable(connection)
