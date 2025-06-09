# UI
from gui import Application
from gui.manager.routemanager import RouteManager

# Routes
from gui.screens.alunos import Students, EditStudent, CreateStudent
from gui.screens.livros import Books, EditBook, CreateBook
from gui.screens.atendentes import Secretaries, EditSecretary, CreateSecretary
from gui.screens.categorias import Categories, EditCategory, CreateCategory
from gui.screens.emprestimos import Loans, EditLoan, CreateLoan
from gui.screens.grupos import Groups, EditGroup, CreateGroup
from gui.screens.reservas import Reserves, EditReserve, CreateReserve
from gui.screens.suspensoes import Suspensions, EditSuspension, CreateSuspension

from gui.screens.turma import Classes, EditClass, CreateClass

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
        "edit_books": EditBook(app.layout.frame),
        "create_book": CreateBook(app.layout.frame),

        "secretaries": Secretaries(app.layout.frame),
        "edit_atts": EditSecretary(app.layout.frame),
        "create_att": CreateSecretary(app.layout.frame),


        "categories": Categories(app.layout.frame),
        "edit_categories": EditCategory(app.layout.frame),
        "create_category": CreateCategory(app.layout.frame),

        "loans": Loans(app.layout.frame),
        "edit_loans": EditLoan(app.layout.frame),
        "create_loan": CreateLoan(app.layout.frame),

        "groups": Groups(app.layout.frame),
        "edit_groups": EditGroup(app.layout.frame),
        "create_group": CreateGroup(app.layout.frame),

        "reserves": Reserves(app.layout.frame),
        "edit_reserves": EditReserve(app.layout.frame),
        "create_reserve": CreateReserve(app.layout.frame),

        "suspensions": Suspensions(app.layout.frame),
        "edit_suspensions": EditSuspension(app.layout.frame),
        "create_suspension": CreateSuspension(app.layout.frame),

        "classes": Classes(app.layout.frame),
        "edit_classes": EditClass(app.layout.frame),
        "create_class": CreateClass(app.layout.frame),
    }
    RouteManager.app = app

    app.initialize()
    app.mainloop()
