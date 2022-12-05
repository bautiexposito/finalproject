# Proyecto final de Programacion II - rusopro
# Bautista Exposito, Felipe Garcia, Rocio Woscoff

import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus

app = Flask(__name__)

with open("biblioteca.json",encoding='utf-8') as archivo_json:
    peliculas=json.load(archivo_json)
peliculas=peliculas[0]['peliculas']

#print(peliculas)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/peliculas")
def devolver_peliculas():
    return jsonify(peliculas)

@app.route("/peliculas/<id>")
def devolver_peliculas(id):
    id_int=int(id)
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            return jsonify(pelicula)
    return Response("{}", status=HTTPStatus.NOT_FOUND)