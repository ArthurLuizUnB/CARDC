import hashlib
from .database_config import db # NOVO: Importa o objeto db

class Usuario(db.Model): # NOVO: Herda de db.Model
    __tablename__ = 'usuarios' # Define o nome da tabela no BD
    
    # Colunas da Tabela
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) # Aumentado para acomodar o hash
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome_completo = db.Column(db.String(120), nullable=True)
    biografia = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    caminho_foto_perfil = db.Column(db.String(255), nullable=True)
    
    # NOVO: Relacionamento com Ciclos. 'backref' permite acessar o usuário a partir de um ciclo.
    ciclos = db.relationship('CicloDeEstudo', backref='autor', lazy=True) 

    # Removemos o método __init__
    
    def __repr__(self):
        return f"<Usuario {self.id}: {self.username}>"
        