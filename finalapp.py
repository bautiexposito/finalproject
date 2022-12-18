# Proyecto final de Programacion II - rusopro
# Bautista Exposito, Felipe Garcia, Rocio Woscoff

import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
#   python -m flask run

app = Flask(__name__)

with open("biblioteca.json",encoding='utf-8') as biblioteca_json:
    peliculas=json.load(biblioteca_json)
peliculas=peliculas[0]['peliculas']

with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']


#   log in 
usuario=input("Usuario: ")
contraseña=input("Contraseña: ")
login=False

for u in usuarios:
    if(u["usuario"]==usuario):
        for c in usuarios:
            if(c["contraseña"]==contraseña):
                login=True

if login==True:  
    print("Bienvenido!")
else:  
    print("Error al iniciar sesion")


def generos_imprimir():
    for pelicula in peliculas:
        print(pelicula['genero'])


def directores_imprimir():
    for pelicula in peliculas:
        print(pelicula['directores'])


#def imprimir(archivo): 


@app.route("/")
def home():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula['titulo'])
    return mostrar_peliculas


@app.route("/peliculas")
def devolver_peliculas():
    return jsonify(peliculas)


@app.route("/peliculas/<id>")
def devolver_pelicula(id):
    id_int=int(id)
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            return jsonify(pelicula)
    return Response("{}", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas/delete",methods=["DELETE"])
def eliminar_pelicula():
    datos=request.get_json()
    if "id" in datos:
        for pelicula in peliculas:
            if pelicula["id"] == datos["id"]:
                print("ENCONTRADO")
                del pelicula  # 'del' es delete
                #print(peliculas)
                return Response(status=HTTPStatus.OK)
            else:
                return Response("{}",status=HTTPStatus.BAD_REQUEST)


# @app.route("/peliculas", methods=["POST"]) #hacer
# def comprar_entrada():
#     # recibir los datos de los clientes
#     datos=request.get_json()
#     id=peliculas[-1]['id']
#     id=id+1
#     if ("nombre" in datos and "apellido" in datos):
#         if ("titulo" in datos):
#             peliculas.append({
#                 "id":10,
#                 "titulo":"Avatar 2",
#                 "año":"2022",
#                 "director":"James Cameron",
#                 "sinopsis":"Jake Sully y Ney'tiri han formado una familia y hacen todo lo posible por permanecer juntos. Sin embargo, deben abandonar su hogar y explorar las regiones de Pandora cuando una antigua amenaza reaparece.",
#                 "link":"https://"
#             })
#         imprimir(peliculas)
#         return Response(datos["nombre"],status=HTTPStatus.OK)
#     else:
#         return Response("{}",status=HTTPStatus.BAD_REQUEST)


# @app.route("/peliculas/actualizar", methods=["PUT"]) #hacer
# def modificar_pelicula():
#     datos=request.get_json()
#     if 'id' in datos:
#         for pelicula in peliculas:
#             if pelicula['id']==datos['id']:
#                 print('ENCONTRADO')
#                 if 'sector' in datos:
#                     print('SECTOR')
#                     pelicula['recital']['ticket']['sector']=datos['sector']
#                 elif 'cantidad' in datos:
#                     pelicula['recital']['ticket']['cantidad']=datos['cantidad']
#                 else:
#                     return Response("{}",status=HTTPStatus.BAD_REQUEST)
#         return Response(status=HTTPStatus.OK)
#     else:
#         return Response("{}",status=HTTPStatus.BAD_REQUEST)