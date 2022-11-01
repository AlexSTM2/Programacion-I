import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import routes
from dotenv import load_dotenv
from flask_login import LoginManager, login_required

login_manager = LoginManager()

#Mètodo que inicializa todos los mòdulos
def create_app():
    #Inicializa Flask
    app = Flask(__name__, static_url_path='/static')
    #Cargar variables de entorno 
    load_dotenv()

    app.config['API_URL'] = os.getenv('API_URL')
    login_manager.init_app(app)

    app.register_blueprint(routes.app)
    return app

