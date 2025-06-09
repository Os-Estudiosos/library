# UI
from gui import Application
from gui.manager.routemanager import RouteManager

# Routes
from gui.screens.alunos import Students, EditStudent, CreateStudent

from gui.screens.livros import Books
from gui.screens.atendentes import Secretaries
from gui.screens.categorias import Categories
from gui.screens.emprestimos import Loans
from gui.screens.grupos import Groups
from gui.screens.reservas import Reserves
from gui.screens.suspensoes import Suspensions

from gui.screens.turma import Classes, EditClass, CreateClass, SeeClass

# Configurations
from config.database import *

# Tables and Connections
# from database import Connection

if __name__ == "__main__":
    app = Application(fg_color="#ffffff")

    RouteManager.routes = {  # Definindo minhas telas
        "students": Students(app.layout.frame),
        "edit_students": EditStudent(app.layout.frame),
        "create_student": CreateStudent(app.layout.frame),

        "books": Books(app.layout.frame),
        "secretaries": Secretaries(app.layout.frame),
        "categories": Categories(app.layout.frame),
        "loans": Loans(app.layout.frame),
        "groups": Groups(app.layout.frame),
        "reserves": Reserves(app.layout.frame),
        "suspensions": Suspensions(app.layout.frame),

        "classes": Classes(app.layout.frame),
        "edit_classes": EditClass(app.layout.frame),
        "create_class": CreateClass(app.layout.frame),
        "see_class": SeeClass(app.layout.frame)
    }
    RouteManager.app = app

    app.initialize()
    app.mainloop()
