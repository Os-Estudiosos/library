class RouteManager:
    default = "students"  # A minha rota padrão
    active = "students"  # Minha rota ativa
    routes = {  # Quais são as minhas rotas

    }
    history = []  # Meu histórico de telas
    app = None  # Meu aplicativo mestre

    @classmethod
    def change_active(cls, active):
        cls.active = active
    
    @classmethod
    def go_to(cls, route, arguments=None):
        cls.change_active(route)
        cls.app.delete_previous_screen()
        cls.app.layout.build()
        cls.routes[route].build(arguments)
        