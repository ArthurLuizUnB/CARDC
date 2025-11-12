# MusicBeta_V02/Main/tests/conftest.py
import sys
import os

# ==================================================================
# || INÍCIO DA MUDANÇA (Correção do ImportError)
# ==================================================================
# Pega o caminho do diretório 'tests' (onde este arquivo está)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Pega o caminho do diretório 'Main' (um nível acima)
main_dir = os.path.dirname(current_dir)

# Adiciona o diretório 'Main' ao path do Python
# Esta é a pasta que contém app.py, routes/, models/, etc.
sys.path.insert(0, main_dir)
# ==================================================================
# || FIM DA MUDANÇA (sys.path)
# ==================================================================

import pytest

# ==================================================================
# || INÍCIO DA MUDANÇA (Imports)
# ==================================================================
# Como 'Main' é a nossa raiz agora, importamos diretamente
from app import app as flask_app
from models.database_config import Session, Base
# ==================================================================
# || FIM DA MUDANÇA (Imports)
# ==================================================================

from sqlalchemy import create_engine

@pytest.fixture(scope='session')
def app():
# ... (o resto do ficheiro permanece igual)
    """Configura o app Flask para testes com um BD em memória."""
    
    # Força o uso de um banco de dados SQLite em memória para testes
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    # Configura chaves dummy para testes
    os.environ['SECRET_KEY'] = 'test_secret_key'
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'test_cloud'
    os.environ['CLOUDINARY_API_KEY'] = 'test_key'
    os.environ['CLOUDINARY_API_SECRET'] = 'test_secret'

    # Recria a engine com o BD em memória
    engine = create_engine(os.environ['DATABASE_URL'])
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    
    # Cria todas as tabelas
    Base.metadata.create_all(engine)

    yield flask_app

    # Limpa depois dos testes
    Base.metadata.drop_all(engine)
    Session.remove()

@pytest.fixture
def client(app):
    """Um cliente de teste para o app."""
    return app.test_client()

@pytest.fixture(autouse=True)
def db_session(app):
    """Garante que cada teste rode em uma transação limpa."""
    
    # Limpa a sessão antes de cada teste
    Session.remove()
    # Recria as tabelas para garantir um estado limpo
    Base.metadata.create_all(Session.bind)
    
    yield Session

    # Limpa depois de cada teste
    Session.remove()
    Base.metadata.drop_all(Session.bind)