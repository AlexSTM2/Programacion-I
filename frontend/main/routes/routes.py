#Aquí agrego las rutas de la aplicación
from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions as f   

app = Blueprint('main', __name__, url_prefix= '/')

@app.route('/')
def index():
    return render_template('menu_principal.html')

@app.route('/usr')
def index_usr(jwt = None):
    if jwt == None:
        jwt = f.obtener_jwt()
        
    resp = f.obtener_poemas(jwt=jwt)
    poemas = f.obtener_json(resp)
    lista_poemas = poemas["Poemas"]
    usuario = f.obtener_usuario(f.obtener_id())
    usuario = json.loads(usuario.text)
    return render_template('menu_principal_usuario.html', poemas = lista_poemas, jwt = jwt, usuario = usuario)

@app.route('/login', methods = ["GET", "POST"])
def login():

    if(request.method == "POST"):

        email = request.form.get("email")
        password = request.form.get("password")

        if email != None and password != None:

            response = f.login(email, password)

            if (response.ok):
                response = json.loads(response.text)
                token = response["Token de acceso"]
                user_id = str(response["ID Usuario"])

                resp = make_response(index_usr(jwt=token))
                resp.set_cookie("Token de acceso", token)
                resp.set_cookie("ID Usuario", user_id)

                return resp
            
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("login.html")



@app.route('/ver-poema')
def ver_poema_publico():
    return render_template('datos_poema_publico.html')

@app.route('/ver-poema-usuario/<int:id>')
def ver_poema_usuario(id):
    jwt = f.obtener_jwt()
    if jwt == None:
        return redirect(url_for('main.login'))
    else:
        usuario = f.obtener_usuario(f.obtener_id())
        usuario = json.loads(usuario.text)
        resp = f.obtener_poema(id)
        poema = f.obtener_json(resp)
        return render_template('datos_poema_usuario.html', poema = poema, usuario=usuario)


@app.route('/ver-calif-publico')
def ver_calif_publico():
    return render_template('ver_calif_publico.html')

@app.route('/ver-calif-usuario')
def ver_calif_usuario():
    return render_template('ver_calif_usuario.html')

@app.route('/subir_poema', methods = ["GET", "POST"])
def subir_poema():

    jwt = f.obtener_jwt()
    id = f.obtener_id()
    usuario = f.obtener_usuario(id)
    usuario = json.loads(usuario.text)
    poemas = f.obtener_poemas_id(id=id)
    poemas = f.obtener_json(poemas)
    lista_poemas = poemas["Poemas"]

    if jwt:
        if(request.method == "POST"):
            titulo = request.form.get("titulo")
            cuerpo = request.form.get("form_poema")
            if titulo != "" and cuerpo != "":
                data = {"id_usuario": id, "titulo": titulo, "cuerpo": cuerpo}
                headers = f.obtener_headers(without_token=False)
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                
                if response.ok:
                    return render_template("mis_poemas.html", usuario = usuario, poemas=lista_poemas)
            else:
                return render_template("subir_poema.html", error="No se pudo subir el poema")
        else:
            return render_template("subir_poema.html", usuario = usuario, poemas = lista_poemas)
    else:    
        return render_template("subir_poema.html")

@app.route('/mi-perfil')
def mi_perfil():
    return render_template('mi_perfil.html')

@app.route('/mis_poemas')
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