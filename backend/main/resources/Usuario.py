from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloUsuario

class Usuario(Resource):

    def get(self, id):
        usuario = db.session.query(ModeloUsuario).get_or_404(id)
        return usuario.to_json()
        
    def delete(self, id):
        usuario =  db.session.query(ModeloUsuario).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

    def put(self, id):

        usuario = db.session.query(ModeloUsuario).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

class Usuarios(Resource):
    #Obtener lista de recursos
    def get(self):
        
        usuarios = db.session.query(ModeloUsuario).all()
        return jsonify([usuario.to_json_short() for usuario in usuarios])

    #Insertar recurso
    def post(self):
        usuario = ModeloUsuario.from_json(request.get-json())
        db.session.add(usuario)
        db.commit()
        return usuario.to_json(), 201