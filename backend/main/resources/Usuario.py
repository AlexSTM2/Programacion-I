from flask_restful import Resource
from flask import request, jsonify
from .. import db
from sqlalchemy import func
from main.models import ModeloUsuario, ModeloPoema, ModeloCalificacion
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Usuario(Resource):

    #Obtener recurso
    @jwt_required(optional=True)
    def get(self, id):

        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                usuario = db.session.query(ModeloUsuario).get_or_404(id)
                return usuario.to_json()
            else:
                usuario = db.session.query(ModeloUsuario).get_or_404(id)
                return usuario.to_json_public()
        else:
            usuario = db.session.query(ModeloUsuario).get_or_404(id)
            return usuario.to_json_public()

    #Eliminar recurso
    @jwt_required()
    def delete(self, id):
        id_usuario = get_jwt_identity()
        usuario =  db.session.query(ModeloUsuario).get_or_404(id)
        claims = get_jwt()
        if claims['rol'] == "admin" or id_usuario == int(id):
            
            db.session.delete(usuario)
            db.session.commit()
            return '', 204
        else:
            return 'Este usuario no puede realizar esa acción', 403
            
    #Modificar recurso
    @jwt_required()
    def put(self, id):
        id_usuario = get_jwt_identity()
        claims = get_jwt()
        if claims['rol'] == "admin" or id_usuario == int(id):
            
            usuario = db.session.query(ModeloUsuario).get_or_404(id)
            data = request.get_json().items()
            for key, value in data:
                setattr(usuario, key, value)
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        else:
            return 'Este usuario no puede realizar esa acción', 403

class Usuarios(Resource):
    #Obtener lista de recursos
    @admin_required
    def get(self):
        
        usuarios = db.session.query(ModeloUsuario)
        page = 1
        per_page = 2
        #Hago el request y los filtros
        if request.get_json():
            filtros = request.get_json().items()
            for key, value in filtros:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "nombre_us":
                    usuarios = usuarios.filter(ModeloUsuario.nombre.like("%"+ value +"%"))
                
                #Estos son los ordenamientos
                if key == "ordenar_por":
                    if value == "nombre_autor":
                        usuarios = usuarios.order_by(ModeloUsuario.nombre)
                    if value == "nombre_autor[desc]":
                        usuarios = usuarios.order_by(ModeloUsuario.nombre.desc())
                    if value == "cant_poemas":
                        usuarios = usuarios.outerjoin(ModeloUsuario.poemas).group_by(ModeloUsuario.id).order_by(func.count(ModeloPoema.id))
                    if value == "cant_poemas[desc]":
                        usuarios = usuarios.outerjoin(ModeloUsuario.poemas).group_by(ModeloUsuario.id).order_by(func.count(ModeloPoema.id).desc())
                    if value == "cant_calificaciones":
                        usuarios = usuarios.outerjoin(ModeloUsuario.calificaciones).group_by(ModeloUsuario.id).order_by(func.count(ModeloCalificacion.id))
                    if value == "cant_calificaciones[desc]":
                        usuarios = usuarios.outerjoin(ModeloUsuario.calificaciones).group_by(ModeloUsuario.id).order_by(func.count(ModeloCalificacion.id).desc())
        #Este es el paginado
        usuarios = usuarios.paginate(page=page, per_page=per_page)
        return jsonify({'Usuarios':[usuario.to_json_short() for usuario in usuarios.items],
        'Total' : usuarios.total, 
       'Páginas': usuarios.pages, 
       "Página" : page})

    #Insertar recurso
    @admin_required
    def post(self):
        usuario = ModeloUsuario.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201