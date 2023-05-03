from flask import request, current_app, url_for, redirect
import requests, json

def obtener_poemas_id(id, page = 1, per_page = 10):

    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "per_page": per_page, "usuario_id": id}
    headers = obtener_headers(without_token = True)
    return requests.get(api_url, json = data, headers = headers)


#Obtengo un poema en especifico.
def obtener_poema(id, without_token = False):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = obtener_headers(without_token)
    return requests.get(api_url, headers=headers)


#Obtengo todos los poemas de la base de datos.
def obtener_poemas(jwt = None, page=1, per_page=5):

    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "per_page": per_page}
    
    if jwt:
        headers = obtener_headers(jwt=jwt)
    else:
        headers = obtener_headers(without_token = True)

    return requests.get(api_url, json=data, headers=headers)


#Obtener un usuario en especifico.
def obtener_usuario(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = obtener_headers()
    return requests.get(api_url, headers=headers)


#Obtengo el nombre del usuario
def obtener_nombre(id_usuario):
    headers = obtener_headers()
    api_url = f'{current_app.config["API_URL"]}/usuario/{id_usuario}'
    response = requests.get(api_url, headers=headers)
    usuario = json.loads(response.text)
    return usuario["nombre"]



#Obtener las calificaciones por poema
def calificaciones_poema(id):
    api_url = f'{current_app.config["API_URL"]}/calificaciones'

    data = {"ID_Poema": id}
    headers = obtener_headers(without_token = True)
    return requests.get(api_url, json = data, headers = headers)

def obtener_mis_calificaciones(id):

    api_url = f'{current_app.config["API_URL"]}/calificaciones'
    headers = obtener_headers(without_token=True)
    data = {'ID_Usuario': int(id)}
    return requests.get(api_url,json=data,headers = headers)

def obtener_calificacion(id):

    api_url = f'{current_app.config["API_URL"]}/calificacion/{id}'
    headers = obtener_headers(without_token=True)
    data = {'id': int(id)}
    return requests.get(api_url,json=data,headers = headers)

#Obtengo el json txt.
def json_load(response):
    return json.loads(response.text)


def obtener_headers(without_token = False, jwt = None):
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
    elif jwt == None and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {obtener_jwt()}"}
    else:
        return {"Content-Type" : "application/json"}


#Obtener el token desde response.
def obtener_jwt():
    return request.cookies.get("Token de acceso")


#Obtener el id desde response.
def obtener_id():
    return request.cookies.get("ID Usuario")


#Hacer redirect

def redirect_to(url):
    return redirect(url_for(url))

def login(email, contraseña):
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    data = {"email": email, "contraseña": contraseña}
    headers = obtener_headers(without_token = True)
    return requests.post(api_url, json = data, headers = headers)

def obtener_json(resp):
    return json.loads(resp.text)