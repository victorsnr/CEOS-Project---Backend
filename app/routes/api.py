from sqlalchemy.exc import IntegrityError

from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Task
from datetime import date, datetime

api = Blueprint('api', __name__)


@api.route("/cadastrar_usuario", methods = ['POST'])
def cadastrar_usuario():
    # Dados da requisição
    data = request.json
    
    nome = data["nome"]
    email = data["email"]
    cpf = data["cpf"]
    dt_nasc = datetime.strptime(data["dt_nasc"], '%Y-%m-%d').date()
    password = data["password"]

    #Tratamento de dados inexistentes
    if not nome or not email or not cpf or not dt_nasc or not password:
        return jsonify({'message': "Erro! Dados inexistentes!"}), 400
    
    #Tratamento de nome
    for caractere in nome:
        if caractere.isdigit():
            return jsonify({'message': 'Erro! Nome não pode conter dígitos!'}), 400
        
    #Tratamento de cpf
    for caractere in cpf:
        if not caractere.isdigit():
            return jsonify({'message': 'Erro! CPF deve conter somente dígitos!'}), 400
        
    if len(cpf) != 11:
        return jsonify({'message': 'Erro! CPF está incompleto'}), 400
    
    #Tratamento de data de nascimento
    data_atual = date.today()
    idade = data_atual.year - dt_nasc.year

    if dt_nasc > data_atual or idade > 110:
        return jsonify({'message': 'Erro! Data inválida!'})
    
    #Tratamento de senha
    if len(password) < 8:
        return jsonify({'message': 'Erro! Senha deve conter 8 dígitos ou mais!'})
    
    
    elif len(password) > 255:
        return jsonify({'message': 'Erro! Senha deve conter 255 dígitos ou menos'})

    #Tratamento de existência
    user_existente = User.query.filter_by(cpf = cpf).first()
    if user_existente:
        return jsonify({'message': 'Erro! CPF já cadastrado'})
     
    user_existente = User.query.filter_by(email = email).first()
    if user_existente:
        return jsonify({'message': 'Erro! Email já cadastrado'})
    
    new_user = User(nome = nome,
                     email = email,
                     cpf = cpf,
                     dt_nasc = dt_nasc,
                     password = password)
    
    #Último teste de integridade
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erro! Possível duplicação de dados! Verifique seu email e CPF'})
    
    return jsonify({
            'message': 'Novo usuário cadastrado com sucesso!',
            'id': new_user.id
        }), 201


    



    
