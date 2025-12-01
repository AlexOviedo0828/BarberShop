from flask_app import app

# Importar TODAS las rutas correctamente
from flask_app.controllers.usuarios import *
from flask_app.controllers.peluqueros import *
from flask_app.controllers.productos import *
from flask_app.controllers.citas import *
from flask_app.controllers.pedidos import *
from flask_app.controllers.admin import *
from flask_app.controllers.horarios import *

if __name__ == "__main__":
    app.run(debug=True, port=5000)
