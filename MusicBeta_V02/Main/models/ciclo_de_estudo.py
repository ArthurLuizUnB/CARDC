import uuid
from .database_config import db # NOVO: Importa o objeto db

class CicloDeEstudo(db.Model): # NOVO: Herda de db.Model
    __tablename__ = 'ciclos_de_estudo'

    # Colunas da Tabela
    id = db.Column(db.String, primary_key=True)
    
    # NOVO: Chave Estrangeira. Linka com a tabela 'usuarios'
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False) 
    
    obra = db.Column(db.String(255), nullable=False)
    compositor = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.String(10), nullable=False)
    data_finalizacao = db.Column(db.String(10), nullable=True)
    link_gravacao = db.Column(db.String(255), nullable=True)
    consideracoes_preliminares = db.Column(db.Text, nullable=True)
    acao_artistica = db.Column(db.Text, nullable=True)
    descricao_tarefa = db.Column(db.Text, nullable=True)
    resultado_tecnico = db.Column(db.Text, nullable=True)
    resultado_musical = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    pensamentos_associados = db.Column(db.Text, nullable=True)
    emocoes_associadas = db.Column(db.Text, nullable=True)
    diario_reflexivo = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="em_andamento")
    capa_url = db.Column(db.String(255), nullable=True)

    # Removemos o método __init__
    
    def __repr__(self):
        return f"<CicloDeEstudo {self.id}: {self.obra}>"

