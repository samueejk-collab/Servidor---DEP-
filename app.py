from flask import Flask, request, jsonify
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
    resultado = []
    try:
        cursor = db.execute("""SELECT id, nombre, valor,
                            datetime(fecha_hora, '-3 hours') 
                            AS fecha_hora 
                            FROM lecturas;""")
        resultado = cursor.fetchall()
    finally:
        db.close()
             
    return jsonify(resultado)

@app.route('/api/sensor', methods=['POST'])
def recibir_datos():
    datos = request.json
    nombre = datos['nombre']
    valor = datos['valor']
    
    db = sqlite3.connect(ARCHIVO_BD)
    db.row_factory = make_dicts
    try:
        db.execute("""INSERT INTO lecturas(nombre,valor) 
                   VALUES (?, ?);""",(nombre, valor)) #esto por si acaso el usuario ponga algo en riego la bsae de datos       
        db.commit()    #segurida pa q n pingan lo q deseen
    finally:
        db.close()
         
    ##
    return 'OK'