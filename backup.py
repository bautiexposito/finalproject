import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
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