# app.py

from flask import Flask, g, current_app 
from routes.routes import routes
from datetime import datetime
import os 
import uuid 
# REMOVIDO: from models.database_config import db 
from models.bcrypt_config import bcrypt # Assumindo que este arquivo existe
from models.database_config import Base, Session # NOVO: Importa Base e Session
from sqlalchemy import create_engine
import atexit 

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

# 3. GERENCIAMENTO DE SESSÃO SQLALCHEMY (NOVO)
engine = create_engine(DATABASE_URI, convert_unicode=True)
Session.configure(bind=engine)
Base.metadata.bind = engine

# FECHA A SESSÃO APÓS CADA REQUEST (TEARDOWN)
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# GARANTE QUE A ENGINE SEJA FECHADA AO DESLIGAR
atexit.register(lambda: engine.dispose())

# FUNÇÃO PARA CRIAR AS TABELAS
def init_db():
    from models import usuario, ciclo_de_estudo 
    Base.metadata.create_all(bind=engine)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        init_db() # Cria as tabelas
    app.run(host="0.0.0.0", port=5000, debug=True)