from flask import Flask, g, current_app 
from routes.routes import routes
from datetime import datetime
import os 
import uuid 
from models.bcrypt_config import bcrypt 
from models.database_config import Base, Session 
from sqlalchemy import create_engine
import atexit 
from models import usuario, ciclo_de_estudo, gravacao
from helpers.mail_config import mail

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

# FUNÇÃO DE CRIAÇÃO DE TABELAS (para ser chamada externamente)
def init_db():
    Base.metadata.create_all(bind=engine)

# O Render vai fornecer esses valores via variáveis de ambiente
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# 2. INICIALIZAÇÃO DE EXTENSÕES
bcrypt.init_app(app)
mail.init_app(app) # NOVO: Inicializa o Mail    

# FECHA A SESSÃO APÓS CADA REQUEST (TEARDOWN)
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# GARANTE QUE A ENGINE SEJA FECHADA AO DESLIGAR
atexit.register(lambda: engine.dispose())

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    # Mantém esta função apenas para desenvolvimento local
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)