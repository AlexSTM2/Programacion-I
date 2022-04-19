import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
#Inicio API de Flask restful
api = Api()
#Mètodo que inicializa todos los mòdulos
#Inicio SQLAlchemy
db = SQLAlchemy()

def create_app():
    #Inicializa Flask
    app = Flask(__name__)
    #Cargar variables de entorno 
    load_dotenv()
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)
    #Importo directorio de recursos
    import main.resources as resources
    api.add_resource(resources.RecursoUsuario, "/usuario/<id>")
    api.add_resource(resources.RecursoUsuarios, "/usuarios" )
    api.add_resource(resources.RecursoPoema, "/poema/<id>" )
    api.add_resource(resources.RecursoPoemas, "/poemas" )
    api.add_resource(resources.RecursoCalificacion, "/calificacion/<id>")
    api.add_resource(resources.RecursoCalificaciones, "/calificaciones")
    #Cargar la aplicaciòn en la API de Flask Restful
    api.init_app(app)
    return app