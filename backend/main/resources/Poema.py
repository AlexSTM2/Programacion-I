from datetime import datetime
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from sqlalchemy import func
from main.models import ModeloPoema, ModeloUsuario, ModeloCalificacion
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Poema(Resource):

    @jwt_required(optional=True)
    def get(self, id):

        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                poema = db.session.query(ModeloPoema).get_or_404(id)
                return poema.to_json()
            else:
                poema = db.session.query(ModeloPoema).get_or_404(id)
                return poema.to_json_public()
        else:
            poema = db.session.query(ModeloPoema).get_or_404(id)
            return poema.to_json_public()

    @jwt_required()           
    def delete(self, id):
        
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        poema = db.session.query(ModeloPoema).get_or_404(id)
        if "rol" in claims:
            if claims['rol'] == "admin" or id_usuario == int(poema.usuario.id):
                db.session.delete(poema)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no puede realizar esa acción"

class Poemas(Resource):

    #Obtener lista de recursos
    @jwt_required(optional=True)
    def get(self):
        page = 1
        per_page = 3
        poemas = db.session.query(ModeloPoema)
        claims = get_jwt()
        identificador_usu = get_jwt_identity()
        if identificador_usu:
            if request.get_json():
                filtros = request.get_json().items()
                for key, value in filtros:
                        if key == "page":
                            page = int(value)
                        if key == "per_page":
                            per_page = int(value)
            poemas = db.session.query(ModeloPoema).filter(ModeloPoema.usuario_id != identificador_usu)
            poemas = poemas.outerjoin(ModeloPoema.calificaciones).group_by(ModeloPoema.id).order_by(func.count(ModeloPoema.calificaciones))
        
        else:
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
                        if key == "puntaje":
                            poemas = poemas.outerjoin(ModeloPoema.calificaciones).group_by(ModeloPoema.id).having(func.avg(ModeloCalificacion.puntaje) <= float(value))
                        if key == "puntaje[desc]":
                            poemas = poemas.outerjoin(ModeloPoema.calificaciones).group_by(ModeloPoema.id).having(func.avg(ModeloCalificacion.puntaje) >= float(value))
                        
                        #Estos son los ordenamientos
                        if key == "ordenar_por":
                            if value == "fecha":
                                poemas = poemas.order_by(ModeloPoema.fecha)
                            if value == "fecha[desc]":
                                poemas = poemas.order_by(ModeloPoema.fecha.desc())
                            if value == "calificaciones":
                                poemas = poemas.outerjoin(ModeloPoema.calificaciones).group_by(ModeloPoema.id).order_by(func.avg(ModeloCalificacion.puntaje))
                            if value == "calificaciones[desc]":
                                poemas = poemas.outerjoin(ModeloPoema.calificaciones).group_by(ModeloPoema.id).order_by(func.avg(ModeloCalificacion.puntaje).desc())
                            if value == "nombre_autor":
                                poemas = poemas.outerjoin(ModeloPoema.usuario).group_by(ModeloPoema.id).order_by(ModeloUsuario.nombre)
                            if value == "nombre_autor[desc]":
                                poemas =  poemas.outerjoin(ModeloPoema.usuario).group_by(ModeloPoema.id).order_by(ModeloUsuario.nombre.desc()) 
                
        #Paginado
        poemas = poemas.paginate(page=page, per_page=per_page, error_out=False)
        if "rol" in claims:
            if claims["rol"] == "admin":
                return jsonify({'Poemas':[poema.to_json() for poema in poemas.items],
                'Total' : poemas.total, 
                'Páginas': poemas.pages, 
                "Página" : page})
        else:
            return jsonify({'Poemas':[poema.to_json_public() for poema in poemas.items],
            'Total' : poemas.total, 
            'Páginas': poemas.pages, 
            "Página" : page})

    
    #Insertar recurso
    @jwt_required()
    def post(self):

        #Obtener datos de la solicitud
        id_usuario = get_jwt_identity()
        poema = ModeloPoema.from_json(request.get_json())
        usuario = db.session.query(ModeloUsuario).get_or_404(id_usuario)
        claims = get_jwt()

        if "rol" in claims:
            if claims["rol"] == "Poeta" or claims["rol"] == "admin":
                if len(usuario.poemas) == 0 or len(usuario.calificaciones) >= 0:
                    poema.usuario_id = id_usuario
                    db.session.add(poema)
                    db.session.commit()
                    return poema.to_json(), 201
                else:
                    return "No hay suficientes calificaciones por parte de este usuario"
            else:
                return "Este usuario no puede realizar esta acción."
