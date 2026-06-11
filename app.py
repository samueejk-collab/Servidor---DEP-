from flask import Flask, request
import sqlite3
app = Flask(__name__)

ARCHIVO_BD="sensores.db"

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


def  make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
                 
@app.route('/api/lecturas')
def lecturas():
    db = sqlite3.connect(ARCHIVO_BD)
    db.row_factory = make_dicts
    db.close()

@app.route('/api/sensor', methods=['POST'])
def recibir_valores():
    datos = request.json
    nombres = datos['nombres']
    valor = datos['valor']

    print(f'Mensaje recibido de {request.remote_addr}')
    print(f'Enviado por {nombres}')
    print(f'Valor del sensor: {valor}')

    return 'OK'