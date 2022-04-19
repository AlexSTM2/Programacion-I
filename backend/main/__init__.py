import os
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
#Importo directorio de recursos
import main.resources as resources
from flask_sqlalchemy import SQLAlchemy
api = Api()
#Mètodo que inicializa todos los mòdulos
db = SQLAlchemy()
def create_app():
    if not os.path.exists(os.getenv('DB_PATH')+os.getenv('DB_NAME')):
        os.mknod(os.getenv('DB_PATH')+os.getenv('DB_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DB_PATH')+os.getenv('DB_NAME')
    db.init_app(app)

    #Inicializa Flask
    app = Flask(__name__)
    #Cargar variables de entorno 
    load_dotenv()
    api.add_resource(resources.RecursoUsuario, "/usuario/<id>")
    api.add_resource(resources.RecursoUsuarios, "/usuarios" )
    api.add_resource(resources.RecursoPoema, "/poema/<id>" )
    api.add_resource(resources.RecursoPoemas, "/poemas" )
    api.add_resource(resources.RecursoCalificacion, "/calificacion/<id>")
    api.add_resource(resources.RecursoCalificaciones, "/calificaciones")
    api.init_app(app)
    return app