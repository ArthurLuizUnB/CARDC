# MusicBeta_V02/Main/tests/test_gravacao_controller.py
import pytest
from controllers.gravacao_controller import GravacaoController
from controllers.ciclo_controller import CicloController
from models.gravacao import Gravacao
from models.ciclo_de_estudo import CicloDeEstudo
from models.usuario import Usuario
import uuid
import datetime

# (Requer o fixture 'db_session' do conftest.py)
def test_adicionar_e_listar_gravacao(db_session):
    # 1. Configuração: Crie um usuário e um ciclo
    id_usr = str(uuid.uuid4())
    id_ciclo = str(uuid.uuid4())
    
    usr = Usuario(id=id_usr, username="testuser", password="123", email="test@test.com")
    ciclo = CicloDeEstudo(
        id=id_ciclo, id_usuario=id_usr, obra="Teste", compositor="Teste", data_inicio="2025-01-01"
    )
    db_session.add(usr)
    db_session.add(ciclo)
    db_session.commit()

    # 2. Ação: Adicione duas gravações
    id_grav_1 = str(uuid.uuid4())
    grav_1 = Gravacao(
        id=id_grav_1,
        id_ciclo=id_ciclo,
        url_video="http://video1.com",
        data_envio=datetime.datetime.utcnow() - datetime.timedelta(days=1) # Mais antigo
    )
    GravacaoController.adicionar(grav_1)
    
    id_grav_2 = str(uuid.uuid4())
    grav_2 = Gravacao(
        id=id_grav_2,
        id_ciclo=id_ciclo,
        url_video="http://video2.com",
        data_envio=datetime.datetime.utcnow() # Mais recente
    )
    GravacaoController.adicionar(grav_2)

    # 3. Verificação
    gravacoes_salvas = GravacaoController.listar_por_ciclo(id_ciclo)
    
    assert len(gravacoes_salvas) == 2
    # Verifica se ordenou por data (mais recente primeiro)
    assert gravacoes_salvas[0].url_video == "http://video2.com"
    assert gravacoes_salvas[1].url_video == "http://video1.com"

def test_remover_gravacao(db_session):
    # 1. Configuração: Crie dados
    id_usr = str(uuid.uuid4())
    id_ciclo = str(uuid.uuid4())
    id_grav = str(uuid.uuid4())
    
    usr = Usuario(id=id_usr, username="testuser", password="123", email="test@test.com")
    ciclo = CicloDeEstudo(id=id_ciclo, id_usuario=id_usr, obra="Teste", compositor="Teste", data_inicio="2025-01-01")
    grav = Gravacao(id=id_grav, id_ciclo=id_ciclo, url_video="http://video1.com")
    
    db_session.add_all([usr, ciclo, grav])
    db_session.commit()

    # 2. Ação
    removido = GravacaoController.remover(id_grav)
    
    # 3. Verificação
    assert removido == True
    gravacoes_restantes = GravacaoController.listar_por_ciclo(id_ciclo)
    assert len(gravacoes_restantes) == 0