#Aquí agrego las rutas de la aplicación
from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions as f   

app = Blueprint('main', __name__, url_prefix= '/')

@app.route('/')
def index():
    pagina = request.args.get('pagina', 1, type=int) # obtener el valor de "page" de la URL
    resp = f.obtener_poemas(page=pagina)
    poemas = f.obtener_json(resp)
    lista_poemas = poemas["Poemas"]
    paginacion = f.paginacion(poemas["Páginas"])
    return render_template('menu_principal.html', poemas = lista_poemas, paginacion = paginacion)


@app.route('/usr')
def index_usr(jwt = None):
    if jwt == None:
        jwt = f.obtener_jwt()  
    if jwt != None and jwt != TypeError("Token has expired"):
        usuario = f.obtener_usuario(f.obtener_id())
        usuario = f.obtener_json(usuario)
        resp = f.obtener_poemas()
        poemas = f.obtener_json(resp)
        lista_poemas = poemas["Poemas"]
        return render_template('menu_principal_usuario.html', poemas = lista_poemas, jwt = jwt, usuario = usuario)
    else:
        return redirect(url_for('main.index'))

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

                resp = redirect(url_for('main.index_usr'))
                resp.set_cookie("Token de acceso", token)
                resp.set_cookie("ID Usuario", usuario_id)

                return resp
            
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    jwt = f.obtener_jwt()
    if jwt == None or jwt == TypeError("Token has expired"):
        return redirect(url_for('main.index'))
    else:
        resp = make_response(redirect(url_for("main.index")))
        resp.delete_cookie("Token de acceso")
        resp.delete_cookie("ID Usuario")
        return resp

@app.route('/ver-poema/<int:id>')
def ver_poema(id, jwt=None):
    if jwt == None:
        jwt = f.obtener_jwt()  
    if jwt != None and jwt != TypeError("Token has expired"):
        return redirect(url_for('main.ver_poema_usuario', id=id))
    else:
        resp = f.obtener_poema(id, without_token=True)
        poema = f.obtener_json(resp)
        print("Poema: ", poema)
        return render_template('datos_poema_publico.html', poema=poema)

@app.route('/ver-poema-usuario/<int:id>')
def ver_poema_usuario(id):
    jwt = f.obtener_jwt()
    if jwt == None and jwt != TypeError("Token has expired"):
        return redirect(url_for('main.index'))
    else:
        usuario = f.obtener_usuario(f.obtener_id())
        usuario = f.obtener_json(usuario)
        resp = f.obtener_poema(id)
        poema = f.obtener_json(resp)
        return render_template('datos_poema_usuario.html', poema = poema, usuario=usuario)


@app.route('/ver_calif_publico/<int:id>/<int:id_calif>')
def ver_calif_publico(id, id_calif):
    jwt = f.obtener_jwt()
    if jwt != None and jwt != TypeError("Token has expired"):
        return redirect(url_for('main.ver_calif_usuario', id=id, id_calif=id_calif))
    else:
        poema = f.obtener_poema(id, without_token=True)
        poema = f.obtener_json(poema)
        calif = f.obtener_calificacion(id_calif)
        calif = f.obtener_json(calif)
        print("Calif: ", calif)
        print("Poema: ", poema)
        return render_template('ver_calif_publico.html', poema = poema, calificacion = calif)

@app.route('/ver_calif_usuario/<int:id>/<int:id_calif>')
def ver_calif_usuario(id, id_calif):
    jwt = f.obtener_jwt()
    if jwt != None and jwt != TypeError("Token has expired"):
        poema = f.obtener_poema(id)
        poema = f.obtener_json(poema)
        id_usuario = f.obtener_id()
        usuario = f.obtener_usuario(id_usuario)
        usuario = f.obtener_json(usuario)
        calif = f.obtener_calificacion(id_calif)
        calif = f.obtener_json(calif)
        return render_template('ver_calif_usuario.html', usuario = usuario, poema = poema, calificacion = calif)
    else:
        return redirect(url_for('main.index'))

@app.route('/subir_poema', methods = ["GET", "POST"])
def subir_poema():

    jwt = f.obtener_jwt()

    if jwt:
        id = f.obtener_id()
        usuario = f.obtener_usuario(id)
        usuario = f.obtener_json(usuario)
        if(request.method == "POST"):
            titulo = request.form.get("titulo")
            cuerpo = request.form.get("form_poema")
            if titulo != "" and cuerpo != "":
                data = {"id_usuario": id, "titulo": titulo, "cuerpo": cuerpo}
                headers = f.obtener_headers(without_token=False)
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                
                if response.ok:
                    resp = redirect(url_for('main.mis_poemas'))
                    return resp
            else:
                return render_template("subir_poema.html")
        else:
            return render_template("subir_poema.html", usuario = usuario)
    else:    
        return redirect(url_for('main.index'))


@app.route('/mi_perfil')
def mi_perfil():

    jwt = f.obtener_jwt()
    if jwt:
        usuario = f.obtener_usuario(f.obtener_id())
        usuario = f.obtener_json(usuario)
        return render_template("mi_perfil.html", usuario = usuario)
    else:
        return redirect(url_for('main.index'))
    


@app.route('/mis_poemas')
def mis_poemas():
    jwt = f.obtener_jwt()
    if jwt:
        id = f.obtener_id()
        usuario = f.obtener_usuario(id)
        usuario = f.obtener_json(usuario)
        poemas = f.obtener_poemas_id(id=id)
        poemas = f.obtener_json(poemas)
        lista_poemas = poemas["Poemas"]
        return render_template("mis_poemas.html", usuario = usuario, poemas = lista_poemas)
    else:
        return redirect(url_for('main.index'))

@app.route('/calificar/<int:id_poema>', methods = ["GET", "POST"])
def calificar(id_poema):
    jwt = f.obtener_jwt()
    if jwt:
        id = f.obtener_id()
        usuario = f.obtener_usuario(id)
        usuario = f.obtener_json(usuario)
        poema = f.obtener_poema(id_poema)
        poema = f.obtener_json(poema)

        if(request.method == "POST"):
            puntaje = request.form.get('check_form')
            comentario = request.form.get('form_comentario')
            if puntaje != "" and comentario != "" and poema["Autor"] != usuario["Nombre"]:
                data = {"comentario": comentario, "puntaje": puntaje, "poema_id": id_poema}
                headers = f.obtener_headers(without_token=False)
                response = requests.post(f'{current_app.config["API_URL"]}/calificaciones', json=data, headers=headers)
            
            elif poema["Autor"] == usuario["Nombre"]:
                return render_template('calificar.html', usuario = usuario, poema=poema, error = "No puedes calificar tu propio poema")
            
            if response.ok:
                resp = make_response(redirect(url_for('main.index_usr')))
                return resp
        else:
            return render_template('calificar.html', usuario = usuario, poema=poema)
    else:
        return redirect(url_for('main.index'))
    
    

@app.route('/modif_calif/<int:id_calif>/<int:id_poema>',  methods = ["GET", "POST"])
def modif_calif(id_calif, id_poema, jwt = None):
    jwt = f.obtener_jwt()
    if jwt == None:
        return redirect(url_for('main.index'))
    else:  
        usuario = f.obtener_usuario(f.obtener_id())
        usuario = f.obtener_json(usuario)
        poema = f.obtener_poema(id_poema)
        poema = f.obtener_json(poema)
        calif = f.obtener_calificacion(id_calif)
        calif = f.obtener_json(calif)
        if(request.method == "POST"):
            puntaje = request.form.get('check_form')
            comentario = request.form.get('form_comentario')
            print(comentario, puntaje)
            if puntaje != "" and comentario != "":
                data = {"comentario": comentario, "puntaje": puntaje, "poema_id": id_poema}
                headers = f.obtener_headers(without_token=False)
                response = requests.put(f'{current_app.config["API_URL"]}/calificacion/{id_calif}', json=data, headers=headers)
                
            if response.ok:
                resp = make_response(redirect(url_for('main.index_usr')))
                return resp
            else:
                print(response.text)
        else:
            return render_template('modificar_calif.html', usuario = usuario, poema = poema, calificacion = calif)

@app.route('/modif_perfil', methods = ['GET','POST'])
def modif_perfil():
    jwt = f.obtener_jwt()
    if jwt:
        id = f.obtener_id()
        usuario = f.obtener_usuario(id)
        # email_actual = request.cookies.get("Email")
        usuario = f.obtener_json(usuario)
        email_actual = usuario["Email"]
    
        if(request.method == "POST"):
            nombre = request.form.get("nombre")
            nuevo_email = request.form.get("email")
            contraseña_actual = request.form.get("contraseña_actual")
            nueva_contraseña = request.form.get("contraseña")
            response = f.login(email_actual, contraseña_actual)

            if response.ok:
                if nombre != "" and nuevo_email != "" and nueva_contraseña != "":
                    data = {"nombre": nombre, "email": nuevo_email, "contraseña": nueva_contraseña}
                    headers = f.obtener_headers()
                    response_put = requests.put(f'{current_app.config["API_URL"]}/usuario/{id}', json=data, headers=headers)
                    if response_put.ok:
                        return redirect(url_for('main.mi_perfil'))
                else:
                    return render_template('modificar_mi_perfil.html', usuario = usuario)

        return render_template('modificar_mi_perfil.html', usuario = usuario)
    else:
        return redirect(url_for('main.index'))

@app.route('mis_calif')
def mis_calif():
    jwt = f.obtener_jwt()
    
    if jwt:
        id = f.obtener_id()
        usuario = f.obtener_usuario(id)
        usuario = f.obtener_json(usuario)
        calificaciones = f.obtener_mis_calificaciones(id=id)
        calificaciones = f.obtener_json(calificaciones)
        return render_template("mis_calificaciones.html", usuario = usuario, calificaciones=calificaciones)
    else:
        return redirect(url_for("main.index"))