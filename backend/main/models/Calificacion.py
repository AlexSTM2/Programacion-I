#Importo la base de datos desde el main
from .. import db

class Calificacion(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    puntaje = db.Column(db.Integer(), nullable = False)
    comentario = db.Column(db.String(100), nullable = True)
    #Claves foránea
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'), nullable = False)
    poema_id = db.Column(db.Integer(), db.ForeignKey('poema.id'), nullable = False)
    #Relaciones
    usuario = db.relationship("Usuario", back_populates="calificaciones", uselist=False, single_parent=True)
    poema = db.relationship("Poema", back_populates="calificaciones", uselist=False, single_parent=True)
    def __repr__(self):

        return "<Califiaciòn: %r %r >" % (self.usuario_id, self.puntaje, self.comentario, self.poema_id)
    
    def to_json(self):
        calificacion_json = {
            "id" : self.id ,
            "puntaje" : int(self.puntaje) ,
            "comentario" : str(self.comentario),
            "ID Usuario" : self.usuario_id,
            "ID Poema" : self.poema_id
        }
        return calificacion_json
    
    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario' : str(self.comentario)
        }
        return calificacion_json
    
    @staticmethod
    #Vamos a convertir JSON a objeto
    def from_json(calificacion_json):

        id = calificacion_json.get("id")
        puntaje = calificacion_json.get("puntaje")
        comentario = calificacion_json.get("comentario")
        userid = calificacion_json.get("user id")
        poemaid = calificacion_json.get("poemaid")
        return Calificacion(id = id,
                puntaje = puntaje,
                comentario = comentario,
                userid = userid,
                poemaid = poemaid)