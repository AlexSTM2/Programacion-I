#Importo la base de datos desde el main
from .. import db

class Usuario(db.Model):
#Acà defino las columnas que van a formar a mi tabla de Usuarios, con todos 
#los datos que necesito.

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    contraseña = db.Column(db.String(20), nullable = False)
    rol = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    def __repr__(self):

<<<<<<< HEAD
        return "<Usuario: %r %r >" % (self.nombre, self.rol, self.contraseña, self.id)
=======
        return "<Usuario: %r %r >" % (self.nombre, self.rol, self.email)
>>>>>>> 0fbd1743b49f545cf5be5afc769aacc12bd694c2
    
    def to_json(self):

        usuario_json = {
            "id" : self.id ,
            "nombre" : str(self.nombre) ,
            "rol" : str(self.rol),
            "contraseña" : str(self.contraseña), 
            "email" : str(self.email)
        }
        return usuario_json
    
    def to_json_short(self):
        usuario_json = {
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
        email = usuario_json.get("email")
        return Usuario(id = id,
                nombre = nombre,
                rol = rol,
                contraseña = contraseña,
                email = email)