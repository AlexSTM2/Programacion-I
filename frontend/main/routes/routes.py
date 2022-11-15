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
                usuario_id = str(response["ID Usuario"])

                resp = make_response(index_usr(jwt=token))
                resp.set_cookie("Token de acceso", token)
                resp.set_cookie("ID Usuario", usuario_id)

                return resp
            
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.index")))
    resp.delete_cookie("Token de acceso")
    resp.delete_cookie("ID Usuario")
    return resp

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

@app.route('/ver_calif_usuario/<int:id>/<int:id_calif>')
def ver_calif_usuario(id, id_calif):
    jwt = f.obtener_jwt()
    poema = f.obtener_poema(id)
    poema = f.obtener_json(poema)
    id_usuario = f.obtener_id()
    usuario = f.obtener_usuario(id_usuario)
    usuario = f.obtener_json(usuario)
    calif = f.obtener_calificacion(id_calif)
    calif = f.obtener_json(calif)
    return render_template('ver_calif_usuario.html', usuario = usuario, poema = poema, calificacion = calif)

@app.route('/subir_poema', methods = ["GET", "POST"])
def subir_poema():

    jwt = f.obtener_jwt()
    id = f.obtener_id()
    usuario = f.obtener_usuario(id)
    usuario = json.loads(usuario.text)

    if jwt:
        if(request.method == "POST"):
            titulo = request.form.get("titulo")
            cuerpo = request.form.get("form_poema")
            if titulo != "" and cuerpo != "":
                data = {"id_usuario": id, "titulo": titulo, "cuerpo": cuerpo}
                headers = f.obtener_headers(without_token=False)
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                
                if response.ok:
                    resp = make_response(redirect(url_for('main.mis_poemas')))
                    return resp
            else:
                return render_template("subir_poema.html")
        else:
            return render_template("subir_poema.html", usuario = usuario)
    else:    
        resp = make_response(redirect(url_for('main.index')))
        return resp

@app.route('/mi_perfil')
def mi_perfil():

    jwt = f.obtener_jwt()
    usuario = f.obtener_usuario(f.obtener_id())
    usuario = json.loads(usuario.text)
    
    if jwt:
        return render_template("mi_perfil.html", usuario = usuario)
    else:
        resp = make_response(index())
        return resp
    


@app.route('/mis_poemas')
def mis_poemas():
    jwt = f.obtener_jwt()
    id = f.obtener_id()
    usuario = f.obtener_usuario(id)
    usuario = json.loads(usuario.text)
    poemas = f.obtener_poemas_id(id=id)
    poemas = f.obtener_json(poemas)
    lista_poemas = poemas["Poemas"]
    if jwt:
        return render_template("mis_poemas.html", usuario = usuario, poemas = lista_poemas)
    else:
        resp = make_response(redirect(url_for("main.index")))
        return resp

@app.route('/calificar/<int:id_poema>', methods = ["GET", "POST"])
def calificar(id_poema):
    jwt = f.obtener_jwt()
    id = f.obtener_id()
    usuario = f.obtener_usuario(id)
    usuario = json.loads(usuario.text)
    poema = f.obtener_poema(id_poema)
    poema = f.obtener_json(poema)
    if jwt:
        if(request.method == "POST"):
            puntaje = request.form.get('check_form')
            comentario = request.form.get('form_comentario')
            print(puntaje, comentario)
            if puntaje != "" and comentario != "":
                data = {"comentario": comentario, "puntaje": puntaje, "poema_id": id_poema}
                headers = f.obtener_headers(without_token=False)
                response = requests.post(f'{current_app.config["API_URL"]}/calificaciones', json=data, headers=headers)
            
            if response.ok:
                resp = make_response(redirect(url_for('main.index_usr')))
                return resp

    return render_template('calificar.html', usuario = usuario, poema=poema)
    

@app.route('/modif_calif')
def modificar_cal():
    return render_template('modificar_calif.html')

@app.route('/modif_perfil')
def modificar_perfil():
    return render_template('modificar_mi_perfil.html')

@app.route('mis_calif')
def mis_calif():
    jwt = f.obtener_jwt()
    id = f.obtener_id()
    usuario = f.obtener_usuario(id)
    usuario = json.loads(usuario.text)
    calificaciones = f.obtener_mis_calificaciones(id=id)
    calificaciones = f.obtener_json(calificaciones)
    print("Mis calificaciones", calificaciones)
    if jwt:
        return render_template("mis_calificaciones.html", usuario = usuario, calificaciones=calificaciones)
    else:
        return redirect(url_for("main.index"))