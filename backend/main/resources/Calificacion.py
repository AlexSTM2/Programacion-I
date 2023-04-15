from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloCalificacion, ModeloUsuario
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_mail import Mail
from main.mail.functions import sendMail
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
                return calificacion.to_json()
        else:
            calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
            return calificacion.to_json()
    
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
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        if id_usuario == calificacion.usuario_id or claims["rol"] == "admin":
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
        if request.get_json():
            filtros = request.get_json().items()
            for key, value in filtros:
                if key == "ID_Usuario":
                    return self.calificaciones_usuario(value)
                else:
                    calificaciones = db.session.query(ModeloCalificacion),all()
                    return jsonify([calificacion.to_json() for calificacion in calificaciones])


                    
    def calificaciones_usuario(self, id):
        calificaciones = db.session.query(ModeloCalificacion)
        calificaciones = calificaciones.filter(ModeloCalificacion.usuario.has(ModeloUsuario.id == id)).all()
        return jsonify([calificacion.to_json() for calificacion in calificaciones])

    #Insertar recurso
    @jwt_required()
    def post(self):

        id_usuario = get_jwt_identity()
        calificacion = ModeloCalificacion.from_json(request.get_json())
        usuario_califica = db.session.query(ModeloUsuario).get(id_usuario)
        claims = get_jwt()
        if "rol" in claims:
            if claims['rol'] == "Poeta" or "admin":
                try:
                    calificacion.usuario_id = int(id_usuario)
                    db.session.add(calificacion)
                    db.session.commit()
                    sent = sendMail([calificacion.poema.usuario.email],"Has recibido una calificación",'calificado',usuario_califica = usuario_califica, usuario = calificacion.poema.usuario, poema=calificacion.poema)
                    
                except Exception as error:
                    db.session.rollback()
                    return str(error), 409
                return calificacion.to_json(), 201
            else:
                return "Este usuario no está autorizado para realizar esta acción."
