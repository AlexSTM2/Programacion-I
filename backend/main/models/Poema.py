from .. import db
from datetime import datetime

class Poema(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    #Clave foránea
    usuario_id = db.Column(db.Integer, db.Foreignkey('usuario.id'), nullable=False)

    #Relación
    usuario= db.relationship('Usuario', back_populates='poemas', uselist=False, single_parent=True)
    calificaciones = db.relationship("Calificacion", back_populates="poema", cascade="all, delete-orphan")
    

    cuerpo = db.Column(db.String(1000), nullable = False)
    fecha =db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):

        return "<Usuario: %r %r >" % (self.id, self.titulo, self.cuerpo, self.fecha)
    #Convertir el objeto en JSON
    def to_json(self):

        poema_json = {
            "id" : self.id ,
            "titulo" : str(self.titulo) ,
            "cuerpo" : str(self.cuerpo), 
            'fecha': str(self.fecha.strftime("%d-%m-%Y")),
            "usuario" : self.usuario.to_json_short(),
            'calificaciones' : [calificacion.to_json_short() for calificacion in self.calificaciones]
        }
        return poema_json
    
    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo' : str(self.titulo)

        }
        return poema_json
    
    @staticmethod
    #Vamos a convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get("id")
        titulo = poema_json.get("titulo")
        cuerpo = poema_json.get("cuerpo")
        fecha = poema_json.get("fecha")
        usuario_id = poema_json.get("usuario_id")
        return Poema(id = id,
                titulo = titulo,
                cuerpo = cuerpo,
                fecha = fecha,
                usuario_id = usuario_id)