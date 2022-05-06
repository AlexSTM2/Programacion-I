from flask import request, jsonify, Blueprint
from .. import db
from main.models import ModeloUsuario
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

#Blueprint para acceder a los mètodos de autenticaciòn
auth = Blueprint('auth', __name__, url_prefix= '/auth')

#Logeo

@auth.route('/login', methods=['POST'])
def login():
    #Busca al profesor en la bd por mail
    usuario = db.session.query(ModeloUsuario).filter(ModeloUsuario.email == request.get_json().get("email")).first_or_404()
    #Valida la contraseña
    if usuario.validate_pass(request.get_json().get("contraseña")):
        #Genera un nuevo token
        #Pasa el objeto usuario como identidad
        token_acceso = create_access_token(identity=usuario)
        #Muestro los valores y token
        data = {
            'ID Usuario' : str(usuario.id),
            'Email' : usuario.email,
            'Token de acceso' : token_acceso
        }
        return data, 200
    else:
        return 'Contraseña incorrecta', 401