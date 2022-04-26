#Importo la base de datos desde el main
from .. import db

class Calificacion(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    puntaje = db.Column(db.Integer(), nullable = False)
    comentario = db.Column(db.String(100), nullable = True)
    userid = db.Column(db.Integer(), nullable = False)
    poemaid = db.Column(db.Integer(), nullable = False)

    def __repr__(self):

        return "<Califiaciòn: %r %r >" % (self.userid, self.puntaje, self.comentario)
    
    def to_json(self):

        calificacion_json = {
            "id" : self.id ,
            "puntaje" : int(self.puntaje) ,
            "comentario" : str(self.comentario),
            "user id" : self.userid,
            "poemaid" : self.poemaid
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