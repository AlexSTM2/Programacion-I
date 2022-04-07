from flask_restful import Resource
from flask import request

POEMAS = {1: {"Tìtulo: ": "Pruebas", "Autor: " : "Alexis"}, 2:{"Tìtulo: ": "Pruebas1", "Autor: ": "Alexis"}}

class Poema(Resource):

    def get(self, id):

        if int(id) in POEMAS:
            return POEMAS[int(id)]
        else:
            return '', 404
        
    def delete(self, id):
        
        if int(id) in POEMAS:
            del POEMAS[int(id)]
            return '', 204
        else:
            return '', 404

class Poemas(Resource):
    #Obtener lista de recursos
    def get(self):
        return POEMAS
    #Insertar recurso
    def post(self):
        #Obtener datos de la solicitud
        poema = request.get_json()
        id = int(max(POEMAS.keys())) + 1
        POEMAS[id] = poema
        return POEMAS[id], 201