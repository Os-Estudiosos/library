# UI
from gui import Application

# Configurations
from config.database import *

# Tables and Connections
from database import Connection

if __name__ == "__main__":
    app = Application(fg_color="#ffffff")
    app.initialize()
    app.mainloop()
