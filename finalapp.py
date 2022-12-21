# Proyecto final de Programacion II - rusopro
# Bautista Exposito, Felipe Garcia, Rocio Woscoff

import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
#   $env:FLASK_APP="finalapp.py"
#   python -m flask run

app = Flask(__name__)

with open("biblioteca.json",encoding='utf-8') as biblioteca_json:
    peliculas=json.load(biblioteca_json)
peliculas=peliculas[0]['peliculas']

with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']

with open("directores.json",encoding='utf-8') as directores_json:
    directores=json.load(directores_json)
directores=directores[0]['directores']


@app.route("/")     # Muestra las ultimas 10 peliculas agregadas
def home():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula['titulo'])
    return mostrar_peliculas


@app.route("/usuarios")     # Muestra todos los usuarios
def devolver_usuarios():
    return jsonify(usuarios)


@app.route("/peliculas")   #    Muestra todas las peliculas
def devolver_peliculas():
    return jsonify(peliculas)


@app.route("/peliculas/<id>")   # Muestra las peliculas por id 
def devolver_pelicula(id):
    id_int=int(id)
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            return jsonify(pelicula)
    return Response("{}", status=HTTPStatus.NOT_FOUND)


@app.route("/directores")   # Muestra todos los directores
def directores_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['director'] not in lista:
            lista.append(pelicula['director'])
    return jsonify(lista)


@app.route("/generos")      # Muestra todos los generos
def generos_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['genero'] not in lista:
            lista.append(pelicula['genero'])
    return jsonify(lista)


@app.route("/peliculas/imagen")     # Muestra las peliculas que tienen imagen
def devolver_peliculas_con_imagen():
    dic={}
    for pelicula in peliculas: 
        if "link" in pelicula:
            dic[pelicula['titulo']]=pelicula['link']
    return jsonify(dic)
    

@app.route("/peliculas/director/<id>")      # Muestra todas las peliculas cargadas de un director especifico por id  
def devolver_peliculas_director(id):
    id_int=int(id)
    lista=[]
    for director in directores:
        if id_int==director['id']:
            variable=director['director']
    for pelicula in peliculas:
        if pelicula['director']==variable:
            lista.append(pelicula['titulo'])
    return jsonify(lista)


@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      # Elimina una pelicula por id 
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor:
        return Response(status=HTTPStatus.OK)
    else:  
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/publicar", methods=["POST"])  
def comprar_entrada():
    # recibir los datos de los clientes
    datos=request.get_json()
    id=peliculas[-1]['id']
    id=id+1
    if ("nombre" in datos and "apellido" in datos):
        if ("titulo" in datos):
            peliculas.append({
                "id":10,
                "titulo":"Avatar 2",
                "año":"2022",
                "director":"James Cameron",
                "sinopsis":"Jake Sully y Ney'tiri han formado una familia y hacen todo lo posible por permanecer juntos. Sin embargo, deben abandonar su hogar y explorar las regiones de Pandora cuando una antigua amenaza reaparece.",
                "link":"https://"
            })
        #imprimir(peliculas)
        return Response(datos["nombre"],status=HTTPStatus.OK)
    else:
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/actualizar", methods=["PUT"])    
def modificar_pelicula():
    datos=request.get_json()
    if 'id' in datos:
        for pelicula in peliculas:
            if pelicula['id']==datos['id']:
                print('ENCONTRADO')
                if '' in datos:
                #
                    return Response("{}",status=HTTPStatus.BAD_REQUEST)
        return Response(status=HTTPStatus.OK)
    else:
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


usuario_privado=False
@app.route("/login", methods=["GET"])      # Inicio de sesion 
def inicio_sesion():
    intentos=3
    while intentos>0:
        user=str(input("Ingrese su usuario: "))
        password=str(input("Ingrese su contraseña: "))
        for pelicula in peliculas:
            if user==pelicula["usuario"] and password==pelicula["contraseña"]:
                global usuario_privado
                usuario_privado=True
                break
        intentos-=1
    if intentos==0:
        return("Error al iniciar sesion, limite de intentos.")
