from flask import Flask
from routes.routes import routes
from datetime import datetime
import os 
import uuid 
from models.database_config import db 
from models.bcrypt_config import bcrypt 

app = Flask(__name__, template_folder="views/html")

# --- BLOCO DE CONFIGURAÇÃO (TODAS AS VARIÁVEIS DEVEM VIR AQUI) ---
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24)) 

# 1. Configuração do Banco de Dados
# USA O DRIVER PADRÃO DO PYTHON (SEM PYSQLITE3)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///db.sqlite3'
).replace('postgres://', 'postgresql://') 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
# --- FIM DO BLOCO DE CONFIGURAÇÃO ---


# 2. INICIALIZAÇÃO DE EXTENSÕES
db.init_app(app) 
bcrypt.init_app(app)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        # Cria as tabelas se elas não existirem
        db.create_all()     
    app.run(host="0.0.0.0", port=5000, debug=True)