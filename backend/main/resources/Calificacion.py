from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloCalificacion
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Calificacion(Resource):

    @jwt_required(optional=True)
    def get(self, id):
        
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
                return calificacion.to_json()
            else:
                calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
                return calificacion.to_json_public()
        else:
            calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
            return calificacion.to_json_public()
    
    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        if "rol" in claims:    
            if claims["rol"] == "admin" or id_usuario == calificacion.usuario_id:
                db.session.delete(calificacion)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no está autorizado para realizar esta acción."
    
    @jwt_required()
    def put(self,id):

        id_usuario = get_jwt_identity()
        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        if id_usuario == calificacion.usuario_id:
            data = request.get_json().items()
            for key, value in data:
                setattr(calificacion, key, value)
            
            db.session.add(calificacion)
            db.session.commit() 
            return calificacion.to_json(), 201   
        else:
            return "Este usuario no está autorizado para realizar esta acción."

class Calificaciones(Resource):
    #Obtener lista de recursos
    @jwt_required(optional=True)
    def get(self):
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                calificaciones = db.session.query(ModeloCalificacion).all()
                return jsonify([calificacion.to_json() for calificacion in calificaciones])
            else:
                calificaciones = db.session.query(ModeloCalificacion).all()
                return jsonify([calificacion.to_json_public() for calificacion in calificaciones])    
        else:
            calificaciones = db.session.query(ModeloCalificacion).all()
            return jsonify([calificacion.to_json_public() for calificacion in calificaciones])

    #Insertar recurso
    @jwt_required()
    def post(self):

        calificacion = ModeloCalificacion.from_json(request.get_json())
        claims = get_jwt()
        if "rol" in claims:
            if claims['rol'] == "Poeta":
                id_usuario = get_jwt_identity()
                calificacion.usuario_id = id_usuario
                db.session.add(calificacion)
                db.session.commit()
                return calificacion.to_json(), 201
            else:
                return "Este usuario no está autorizado para realizar esta acción."
