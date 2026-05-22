from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    cpf = db.Column(db.String(11), nullable = False, unique = True)
    dt_nasc = db.Column(db.Date, nullable = False)
    password = db.Column(db.String(255), nullable = False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(300), nullable = False)

    user = db.relationship("User", backref = db.backref('tarefas', lazy = True, cascade = "all, delete-orphan"))

    
    