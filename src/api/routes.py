"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hola has accedido correctamente al endpoint"
    }

    return jsonify(response_body), 200



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():

#Obtener el email y la contraseña del cuerpo de la solicitud JSON
    email = request.json.get("email", None)
    password = request.json.get("password", None)

#Buscar el mail en la base de datos
    user = User.query.filter_by(email=email).first()

#Si mail no existe, devolver un error
    if user is None:
        return jsonify({"msg": "email incorrecto"}), 401

#Si contraseña es incorrecta, devolver mensaje de error
    if password != user.password:
        return jsonify({"msg": "contraseña incorrecta"}), 401

#Crear el token de acceso
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)






@api.route("/signup", methods=["POST"])
def signup():

#Obtener el cuerpo de la solicitud en formato JSON
    body = request.get_json()

#Buscar un usuario en la base de datos con el mail proporcionado
    user = User.query.filter_by(email=body["email"]).first()

#Si no se encuentra ese mail, crear uno nuevo
    if user is None:
#Crear un nuevo usuario con los datos del cuerpo de la solicitud
        user = User(email=body["email"], password=body["password"], is_active=True)
#Añadir el nuevo usuario a la base de datos
        db.session.add(user)
        db.session.commit()

#crear una respuesta diciendo que el usuario se ha creado correctamente
        return jsonify({"msg":"Usuario creado correctamente"}) , 200
    
    else:
#si usuario ya existe, devolver mensaje de error
        return jsonify({"msg":"Ese email ya está registrado"}) , 401
