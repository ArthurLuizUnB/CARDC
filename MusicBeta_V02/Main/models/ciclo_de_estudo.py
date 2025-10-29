# models/ciclo_de_estudo.py

import uuid
from models.database_config import Base # NOVO: Importa Base
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship 

# Novo: Classe herda de Base e define a tabela
class CicloDeEstudo(Base):
    __tablename__ = 'ciclos_de_estudo'

    # Colunas da Tabela
    id = Column(String, primary_key=True)
    # Chave estrangeira ligada à tabela 'usuarios'
    id_usuario = Column(String, ForeignKey('usuarios.id'), nullable=False) 
    
    obra = Column(String(255), nullable=False)
    compositor = Column(String(255), nullable=False)
    data_inicio = Column(String(10), nullable=False)
    data_finalizacao = Column(String(10), nullable=True)
    link_gravacao = Column(String(255), nullable=True)
    consideracoes_preliminares = Column(Text, nullable=True)
    acao_artistica = Column(Text, nullable=True)
    descricao_tarefa = Column(Text, nullable=True)
    resultado_tecnico = Column(Text, nullable=True)
    resultado_musical = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    pensamentos_associados = Column(Text, nullable=True)
    emocoes_associadas = Column(Text, nullable=True)
    diario_reflexivo = Column(Text, nullable=True)
    status = Column(String(20), default="em_andamento")
    capa_url = Column(String(255), nullable=True)

    # Relacionamento para acesso fácil ao autor
    autor = relationship("Usuario", backref="ciclos")

    def __repr__(self):
        return f"<CicloDeEstudo {self.id}: {self.obra}>"
    # REMOVIDOS: __init__ e to_dict