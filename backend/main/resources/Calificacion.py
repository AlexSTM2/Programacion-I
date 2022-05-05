from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloCalificacion


class Calificacion(Resource):

    def get(self, id):

        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        return calificacion.to_json()
        
    def delete(self, id):

        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        db.session.delete(calificacion)
        db.session.commit()
        return '', 204
#Este put no va, pero serìa programado de esta manera:
    def put(self,id):

        calificacion = db.session.query(ModeloCalificacion).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(calificacion, key, value)
        
        db.session.add(calificacion)
        db.session.commit() 
        return calificacion.to_json(), 201   

class Calificaciones(Resource):
    #Obtener lista de recursos
    def get(self):

        calificaciones = db.session.query(ModeloCalificacion).all()
        return jsonify([calificacion.to_json_short() for calificacion in calificaciones])
    #Insertar recurso
    def post(self):

        calificacion = ModeloCalificacion.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201