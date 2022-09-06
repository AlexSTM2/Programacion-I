import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import routes
#Mètodo que inicializa todos los mòdulos
def create_app():
    #Inicializa Flask
    app = Flask(__name__)
    #Cargar variables de entorno 
    load_dotenv()
    app.register_blueprint(routes.app)
    return app

