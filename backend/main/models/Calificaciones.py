#Importo la base de datos desde el main
from .. import db

class Calificacion(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    puntaje = db.Column(db.Integer(100), nullable = False)
    comentario = db.Column(db.String(100), nullable = True)
    userid = db.Column(db.Integer(20), nullable = False)
    poemaid = db.Column(db.Integer(20), nullable = False)

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
            'nombre': str(self.nombre),

        }
        return usuario_json
    
    @staticmethod
    #Vamos a convertir JSON a objeto
    def from_json(usuario_json):

        id = usuario_json.get("id")
        nombre = usuario_json.get("nombre")
        rol = usuario_json.get("rol")
        contraseña = usuario_json.get("contraseña")
        return Usuario(id = id,
                nombre = nombre,
                rol = rol,
                contraseña = contraseña)