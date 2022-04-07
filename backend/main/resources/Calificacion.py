from flask_restful import Resource
from flask import request

CALIFICACIONES = {1: {"Poema: ": "Poema 1", "Calificaciòn: " : "1"}, 2:{"Poema: ": "Poema 2", "Calificaciòn: ": "2"}}

class Calificacion(Resource):

    def get(self, id):

        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        else:
            return '', 404
        
    def delete(self, id):
        
        if int(id) in CALIFICACIONES:
            del CALIFICACIONES[int(id)]
            return '', 204
        else:
            return '', 404

class Calificaciones(Resource):
    #Obtener lista de recursos
    def get(self):
        return CALIFICACIONES
    #Insertar recurso
    def post(self):
        #Obtener datos de la solicitud
        calificacion = request.get_json()
        id = int(max(CALIFICACIONES.keys())) + 1
        CALIFICACIONES[id] = calificacion
        return CALIFICACIONES[id], 201