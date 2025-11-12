# MusicBeta_V02/Main/models/gravacao.py
import uuid
from models.database_config import Base
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

class Gravacao(Base):
    __tablename__ = 'gravacoes'

    # Colunas da Tabela
    id = Column(String, primary_key=True)
    # Chave estrangeira que liga esta gravação a um ciclo de estudo
    id_ciclo = Column(String, ForeignKey('ciclos_de_estudo.id'), nullable=False)
    
    url_video = Column(String(255), nullable=False)
    data_envio = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # Relacionamento (opcional, mas bom para acesso)
    ciclo = relationship("CicloDeEstudo", back_populates="gravacoes")

    def __repr__(self):
        return f"<Gravacao {self.id} do ciclo {self.id_ciclo}>"