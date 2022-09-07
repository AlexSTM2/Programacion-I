#Aquí agrego las rutas
from flask import Blueprint, render_template


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/')
def index():
    return render_template('menu_principal.html')

@app.route('/usr')
def index_usr():
    return render_template('menu_principal_usuario.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/ver-poema')
def ver_poema_publico():
    return render_template('datos_poema_publico.html')

@app.route('/ver-poema-usuario')
def ver_poema_usuario():
    return render_template('datos_poema_usuario.html')

@app.route('/ver-calif-publico')
def ver_calif_publico():
    return render_template('ver_calif_publico.html')

@app.route('/ver-calif-usuario')
def ver_calif_usuario():
    return render_template('ver_calif_usuario.html')

@app.route('/subir-poema')
def subir_poema():
    return render_template('subir_poema.html')

@app.route('/mi-perfil')
def mi_perfil():
    return render_template('mi_perfil.html')

@app.route('/mis-poemas')
def mis_poemas():
    return render_template('mis_poemas.html')

@app.route('/calificar')
def calificar():
    return render_template('calificar.html')

@app.route('/modif_calif')
def modificar_cal():
    return render_template('modificar_calif.html')

@app.route('/modif-perfil')
def modificar_perfil():
    return render_template('modificar_mi_perfil.html')

@app.route('mis-calif')
def mis_calif():
    return render_template('mis_calificaciones.html')