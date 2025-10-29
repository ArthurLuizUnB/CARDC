# app.py (VERSÃO FINAL PARA O DEPLOY)

from flask import Flask, g, current_app 
from routes.routes import routes
from datetime import datetime
import os 
import uuid 
from models.bcrypt_config import bcrypt 
from models.database_config import Base, Session 
from sqlalchemy import create_engine
import atexit 
from models import usuario, ciclo_de_estudo # Importar modelos aqui para garantir que Base os conheça

app = Flask(__name__, template_folder="views/html")

# --- CONFIGURAÇÕES ---
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24)) 

DATABASE_URI = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///db.sqlite3'
).replace('postgres://', 'postgresql://')

app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

# 2. INICIALIZAÇÃO DE EXTENSÕES
bcrypt.init_app(app)

# 3. GERENCIAMENTO DE SESSÃO SQLALCHEMY
engine = create_engine(DATABASE_URI, convert_unicode=True)
Session.configure(bind=engine)
Base.metadata.bind = engine

# FUNÇÃO DE CRIAÇÃO DE TABELAS (para ser chamada na inicialização)
def init_db():
    Base.metadata.create_all(bind=engine)

# FECHA A SESSÃO APÓS CADA REQUEST (TEARDOWN)
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# GARANTE QUE A ENGINE SEJA FECHADA AO DESLIGAR
atexit.register(lambda: engine.dispose())

# CORREÇÃO: CRIAÇÃO DA TABELA NA INICIALIZAÇÃO DO CONTEXTO DO APLICATIVO
with app.app_context():
    init_db() 

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

# REMOVIDO: O bloco if __name__ == "__main__":