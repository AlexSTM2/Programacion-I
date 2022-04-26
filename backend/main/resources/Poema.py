from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloPoema


class Poema(Resource):

    def get(self, id):
        poema = db.session.query(ModeloPoema).get_or_404(id)
        return poema.to_json()

    def delete(self, id):
        poema = db.session.query(ModeloPoema).get_or_404(id)
        db.session.delete(poema)
        db.session.commit()
        return '', 204

class Poemas(Resource):
    #Obtener lista de recursos
    def get(self):
       poemas = db.session.query(ModeloPoema).all()
       return jsonify([poema.to_json_short() for poema in poemas])

    #Insertar recurso
    def post(self):
        #Obtener datos de la solicitud
        poema = ModeloPoema.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201