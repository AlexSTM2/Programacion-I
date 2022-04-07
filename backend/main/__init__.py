import os
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources
api = Api()
#Mètodo que inicializa todos los mòdulos
def create_app():
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