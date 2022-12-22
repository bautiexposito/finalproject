# Proyecto final de Programacion II - rusopro
# Bautista Exposito, Felipe Garcia, Rocio Woscoff

import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import requests
import threading
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


ultimas_peliculas_agregadas=[]
@app.route("/")     # Muestra las ultimas 10 peliculas agregadas
def home():
    if len(ultimas_peliculas_agregadas)>0:
        return jsonify(ultimas_peliculas_agregadas)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/usuarios")     # Muestra todos los usuarios
def devolver_usuarios():
    lista=[]
    for usuario in usuarios:
        lista.append(usuario['usuario'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas")   #    Muestra todas las peliculas
def devolver_peliculas():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula['titulo'])
    if len(mostrar_peliculas)>0:
        return jsonify(mostrar_peliculas)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)    


@app.route("/peliculas/<id>")   # Muestra las peliculas por id 
def devolver_pelicula(id):
    id_int=int(id)
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            return jsonify(pelicula)
    return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/directores")   # Muestra todos los directores
def directores_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['director'] not in lista:
            lista.append(pelicula['director'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/generos")      # Muestra todos los generos
def generos_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['genero'] not in lista:
            lista.append(pelicula['genero'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas/imagen")     # Muestra las peliculas que tienen imagen
def devolver_peliculas_con_imagen():
    dic={}
    for pelicula in peliculas: 
        if "link" in pelicula:
            dic[pelicula['titulo']]=pelicula['link']
    if len(dic)>0:
        return jsonify(dic)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)
    

@app.route("/directores/<id>")      # Muestra todas las peliculas cargadas de un director especifico por id  
def devolver_peliculas_director(id):
    id_int=int(id)
    lista=[]
    for director in directores:
        if id_int==director['id']:
            variable=director['director']
    for pelicula in peliculas:
        if pelicula['director']==variable:
            lista.append(pelicula['titulo'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      # Elimina una pelicula por id 
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor:
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/publicar", methods=["POST"])     # Publica nueva pelicula 
def comprar_entrada():                                  
    datos=request.get_json()                            

    for director in directores:         # Si es un director nuevo lo agrega a directores.json
        id=director['id']
    id+=1
    if datos['director'] not in directores:     
        directores.append({
            "id":id,
            "director":datos['director']
            })

    if len(ultimas_peliculas_agregadas)<10:                 # Agrega las ultimas 10 peliculas a la pagina home
        ultimas_peliculas_agregadas.append(datos['titulo'])     
    else:
        for i in range(9,-1,-1):
            if i != 0:
                ultimas_peliculas_agregadas[i]=ultimas_peliculas_agregadas[i-1]
            ultimas_peliculas_agregadas[0]=datos['titulo'] 

    # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:
    #     json.dump(peliculas,biblioteca_json)

    if (datos['id'] not in peliculas):      # Post
        peliculas.append(datos)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/actualizar", methods=["PUT"])    # Modifica pelicula especifica segun id 
def modificar_pelicula():
    datos=request.get_json()
    if "id" in datos:
        for pelicula in peliculas:
            if(datos['id']==pelicula['id']):
                if "titulo" in datos:
                    pelicula['titulo']=datos["titulo"]
                if "anio" in datos:
                    pelicula['anio']=datos["anio"]
                if "director" in datos:
                    pelicula['director']=datos["director"]
                    if datos['director'] not in directores:
                        for director in directores:
                            id=director['id']
                            id+=1
                        directores.append({
                            "id":id,
                            "director":datos['director']
                        })
                if "genero" in datos:
                    pelicula['genero']=datos["genero"]
                if "sinopsis" in datos:
                    pelicula['sinopsis']=datos["sinopsis"]
                if "link" in datos:
                    pelicula['link']=datos["link"]
                return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


login=False
def menu():
    print("")
    while True:
        print("           MENU             ")
        print("----------------------------")
        print("0: Iniciar/cerrar sesion")#
        print("1: Mostrar todas las peliculas")
        print("2: Mostrar pelicula especifica")#
        print("3: Mostrar ultimas peliculas agregadas")
        print("4: Mostrar peliculas con imagenes")
        print("5: Mostrar directores")
        print("6: Mostrar peliculas de un director especifico")#
        print("7: Mostrar usuarios")#
        print("8: Mostrar generos")
        print("9: Eliminar pelicula")#
        print("10: Publicar pelicula")#
        print("11: Modificar pelicula")#
        print("12: Salir")
        opcion=int(input("Ingresar opcion: "))
        print("")

        if (opcion==0):
            intentos=3
            while intentos>0:
                user=input("Ingresar usuario: ")
                password=input('Ingresar contraseña: ')
                for usuario in usuarios:
                    if(user==usuario['usuario'] and password==usuario['contrasenia']):
                        login=True
                        print("Inicio de sesion exitoso!")
                        break
                intentos-=1
            if intentos==0:
                print("Error al iniciar sesion, limite de intentos.")

        if (opcion==1):
            r=(requests.get("http://127.0.0.1:5000/peliculas"))
            r=dict(r)
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==2):   
            id=int(input("Ingresar id de la pelicula: "))
            r=(requests.get("http://127.0.0.1:5000/peliculas/"+id))
            print(r.text)

        elif (opcion==3):
            r=(requests.get("http://127.0.0.1:5000"))
            print(r.text)

        elif (opcion==4):
            r=(requests.get("http://127.0.0.1:5000/peliculas/imagen"))
            print(r.text)

        elif (opcion==5):
            r=(requests.get("http://127.0.0.1:5000/directores"))
            print(r.text)

        elif (opcion==6): 
            id=int(input("Ingresar id del director: "))
            r=(requests.get("http://127.0.0.1:5000/peliculas/"+id))
            print(r.text)

        elif (opcion==7):
            r=(requests.get("http://127.0.0.1:5000/usuarios"))
            print(r.text)

        elif (opcion==8):
            r=(requests.get("http://127.0.0.1:5000/generos"))
            print(r.text)

        elif (opcion==9):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                print("")

        elif (opcion==10):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                print("")

        elif (opcion==11):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                print("")

        elif (opcion==12):
            print("Exit!\n")
            break
        else:
            print("Error al ingresar opcion")
        print("")

m = threading.Timer(1, menu)    # Ejecutar el menu 1 segundo despues para darle tiempo a crear local server
#m.start()