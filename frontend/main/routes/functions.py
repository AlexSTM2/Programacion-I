from flask import request, current_app, url_for, redirect
import requests, json

def obtener_poemas_id(id, page = 1, per_page = 5):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "per_page": per_page, "usuario_id": id}
    headers = get_headers(without_token = True)
    return requests.get(api_url, json = data, headers = headers)


#Obtengo un poema en especifico.
def obtener_poema(id):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo todos los poemas de la base de datos.
def obtener_poemas(api_url, page=1, per_page=3):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "per_page": per_page}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)


#Obtengo los datos del usuario.
def info_usuario(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtener un usuario en especifico.
def obtener_usuario(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo el nombre del usuario
def obtener_nombre(id_usuario):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}/usuario/{id_usuario}'
    response = requests.get(api_url, headers=headers)
    usuario = json.loads(response.text)
    return usuario["nombre"]



#Obtener las calificaciones
def calificaciones_id(id):
    api_url = f'{current_app.config["API_URL"]}/calificaciones'

    data = {"poema_id": id}
    headers = get_headers()
    return requests.get(api_url, json = data, headers = headers)


#Obtengo el json txt.
def json_load(response):
    return json.loads(response.text)


#Obtengo el email del usuario
def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}


#Obtener el token desde response.
def get_jwt():
    return request.cookies.get("access_token")


#Obtener el id desde response.
def get_id():
    return request.cookies.get("id")


#Hacer redirect

def redirect_to(url):
    return redirect(url_for(url))