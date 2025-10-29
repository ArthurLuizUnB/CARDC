# models/usuario.py

# REMOVIDO: import hashlib
from models.database_config import Base # NOVO
from sqlalchemy import Column, String, Boolean, Text # NOVO

# Novo: Classe herda de Base
class Usuario(Base): 
    __tablename__ = 'usuarios'

    # Colunas da Tabela
    id = Column(String, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(256), nullable=False) 
    email = Column(String(120), unique=True, nullable=False)
    nome_completo = Column(String(120), nullable=True)
    biografia = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False)
    caminho_foto_perfil = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Usuario {self.id}: {self.username}>"

    # REMOVIDOS: __init__, to_dict, hash_password, check_password
    # (bcrypt no controller)