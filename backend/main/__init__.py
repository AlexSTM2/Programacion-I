import os
from flask import Flask
from dotenv import load_dotenv
#Mètodo que inicializa todos los mòdulos
def create_app():
    #Inicializa Flask
    app = Flask(__name__)
    #Cargar variables de entorno 
    load_dotenv()
    return app

