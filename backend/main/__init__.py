import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
#Inicio API de Flask restful
api = Api()

#Mètodo que inicializa todos los mòdulos
#Inicio SQLAlchemy
db = SQLAlchemy()

#Inicializo JWT
jwt = JWTManager()

#Inicio mail
mailsender = Mail()

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
    
    #Cargo la clave secreta
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #Cargo el tiempo de expiraciòn de los tokens
    app.config['JWWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    #Importo el blueprint
    app.register_blueprint(routes.auth)

    #Configuración de mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar en app
    mailsender.init_app(app)
    
    return app