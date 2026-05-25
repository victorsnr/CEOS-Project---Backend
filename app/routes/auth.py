from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User

api_auth = Blueprint('auth', __name__)

@api_auth.route("/login", methods = ["POST"])
def login():
    data = request.json

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username = username).first()

    if not user:
        return jsonify({"message": "Erro! Usuário não encontrado!"}), 404
    
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Erro! Senha inválida!"})
    
    token = create_access_token(identity = str(user.id))

    return jsonify({"access_token": token})
