#Aquí agrego las rutas de la aplicación
from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions as f   

app = Blueprint('main', __name__, url_prefix= '/')

@app.route('/')
def index():
    return render_template('menu_principal.html')

@app.route('/usr')
def index_usr():
    return render_template('menu_principal_usuario.html')

@app.route('/login', methods = ["GET", "POST"])
def login():

    if(request.method == "POST"):
        #Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != None and password != None:
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            #Envio de logueo
            data = {"email": email, "password":password}
            headers = {"Content-Type" : "application/json"}

            response = requests.post(api_url, json=data, headers=headers)

            if (response.ok):
                #Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])


                api_url = f'{current_app.config["API_URL"]}'
                response = f.get_poems(api_url)

                poems = json.loads(response.text)
                list_poems = poems["poems"]
                user = f.get_user(user_id)
                user = json.loads(user.text)

                resp = make_response(render_template("poet_main_page.html", poems=list_poems, user=user, jwt=token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                
                return resp
            
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("login.html")



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