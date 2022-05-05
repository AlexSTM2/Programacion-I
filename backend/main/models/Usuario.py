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
    #Relación
    poemas = db.relationship("Poema", back_populates="usuario", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")
    
    def __repr__(self):

        return "<Usuario: %r %r >" % (self.nombre, self.rol, self.email, self.contraseña)
    
    def to_json(self):

        usuario_json = {
            "ID Usuario" : self.id ,
            "Nombre" : str(self.nombre) ,
            "Rol" : str(self.rol), 
            "Email" : str(self.email),
            "Poemas" : len(self.poemas),
            "Calificaciones" : len(self.calificaciones)

        }
        return usuario_json
    #Este es un llamado completo del usuario, no lo uso actualmente, 
    #pero queda ahí
    def to_json_complete(self):
        usuario_json = {
            "id" : self.id ,
            "nombre" : str(self.nombre) ,
            "rol" : str(self.rol),
            "email" : str(self.email),
            "poemas" : [poema.to_json() for poema in self.poemas],
            "calificaciones" : [calificacion.to_json() for calificacion in self.calificaciones]
        }
        return usuario_json
    
    def to_json_short(self):
        usuario_json = {
            'ID Usuario': self.id,
            'Nombre': str(self.nombre),
            'Rol' : str(self.rol),
            'Poemas' : len(self.poemas),
            'Calificaciones' : len(self.calificaciones)

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