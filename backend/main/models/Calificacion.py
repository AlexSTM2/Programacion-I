#Importo la base de datos desde el main
from email.policy import default
from .. import db

class Calificacion(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    puntaje = db.Column(db.Integer(), nullable = False)
    comentario = db.Column(db.String(100), nullable = True)

    #Claves foránea
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'), nullable = False, unique=True, default=0)
    poema_id = db.Column(db.Integer(), db.ForeignKey('poema.id'), nullable = False)
    
    #Relaciones
    usuario = db.relationship("Usuario", back_populates="calificaciones", uselist=False, single_parent=True)
    poema = db.relationship("Poema", back_populates="calificaciones", uselist=False, single_parent=True)
    def __repr__(self):

        return "<Califiaciòn: %r %r >" % (self.usuario_id, self.puntaje, self.comentario, self.poema_id)
    
    def to_json(self):
        calificacion_json = {
            "ID Calificacion" : self.id ,
            "Puntaje" : int(self.puntaje) ,
            "Comentario" : str(self.comentario),
            "ID Usuario" : self.usuario_id,
            "ID Poema" : self.poema_id
        }
        return calificacion_json

    def to_json_public(self):
        calificacion_json = {
            "Usuario: " : self.usuario.nombre,
            "Poema: " : self.poema.titulo,
            "Puntaje: " : int(self.puntaje),
            "Comentario: " : str(self.comentario)
        }
        return calificacion_json

    def to_json_short(self):
        calificacion_json = {
            "Nombre de usuario" : self.usuario.nombre,
            'ID Calificación': self.id,
            'Puntaje': str(self.puntaje),
            'Comentario' : str(self.comentario),
            'Poema' : self.poema.titulo
        }
        return calificacion_json
    
    @staticmethod
    #Vamos a convertir JSON a objeto
    def from_json(calificacion_json):

        id = calificacion_json.get("id")
        puntaje = calificacion_json.get("puntaje")
        comentario = calificacion_json.get("comentario")
        usuario_id = calificacion_json.get("usuario_id")
        poema_id = calificacion_json.get("poema_id")
        return Calificacion(id = id,
                puntaje = puntaje,
                comentario = comentario,
                usuario_id = usuario_id,
                poema_id = poema_id)