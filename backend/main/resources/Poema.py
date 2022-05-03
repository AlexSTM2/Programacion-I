from datetime import datetime
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ModeloPoema, ModeloUsuario


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
       poemas = db.session.query(ModeloPoema)
       page = 1
       per_page = 3
       #Request y filtros
       if request.get_json():
           filtros = request.get_json().items()
           for key, value in filtros:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "titulo":
                    poemas = poemas.filter(ModeloPoema.titulo.like("%"+value+"%"))
                if key == "usuario_id":
                    poemas = poemas.filter(ModeloPoema.usuario_id == value)
                if key == "fecha[gte]":
                    poemas = poemas.filter(ModeloPoema.fecha >= datetime.strptime(value, "%d-%m-%Y"))
                if key == "fecha[lte]":
                    poemas = poemas.filter(ModeloPoema.fecha <= datetime.strptime(value, "%d-%m-%Y"))
                if key == "nombre_us":
                    poemas = poemas.filter(ModeloPoema.usuario.has(ModeloUsuario.nombre.like("%"+ value +"%")))
       
                #Estos son los ordenamientos
                if key == "ordenar_por":
                    if value == "fecha":
                        poemas = poemas.order_by(ModeloPoema.fecha)
                    if value == "fecha[desc]":
                        poemas = poemas.order_by(ModeloPoema.fecha.desc())
                    if value == "calificaciones":
                        poemas = "Terminar agrupamientos"
       
       #Paginado
       poemas = poemas.paginate(page, per_page, True, 5)
       return jsonify({'Poemas':[poema.to_json_short() for poema in poemas.items],
       'Total' : poemas.total, 
       'Páginas': poemas.pages, 
       "Página" : page})

    #Insertar recurso
    def post(self):
        #Obtener datos de la solicitud
        poema = ModeloPoema.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201