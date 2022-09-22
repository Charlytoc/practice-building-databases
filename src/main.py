"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Jugadores
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/jugadores', methods=['GET'])
def get_jugadores():

    jugadores = Jugadores.query.all()
    
    all_jugadores = list(map(lambda x: x.serialize(), jugadores))
    print(all_jugadores)
    response_body = {
        "msg": "OK "
    }

    return jsonify(response_body), 200

@app.route('/jugadores', methods=['POST'])
def crear_jugador():
    body = request.get_json()
    # print(body)
    
    jugador_nuevo = Jugadores(nombre=body["nombre"], apellido=body["apellido"], equipo_id=body["equipo_id"])
    # db.session.add(user1)
    print(jugador_nuevo.serialize())
    # db.session.commit()
    # all_jugadores = list(map(lambda x: x.serialize(), jugadores))
    # print(all_jugadores)

    response_body = {
        "msg": "OK "
    }

    return jsonify(response_body), 200

@app.route('/jugadores/<int:jugador_id>', methods=['GET'])
def get_one_jugador(jugador_id):

    jugador = Jugadores.query.filter_by(id=jugador_id).first()
    print(jugador.serialize())
    
   
    response_body = {
        "msg": "OK ",
        "result": jugador.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
