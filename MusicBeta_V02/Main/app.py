from flask import Flask
from routes.routes import routes
from datetime import datetime 
import os 
from models.database_config import db
from models.bcrypt_config import bcrypt

app = Flask(__name__, template_folder="views/html")

db.init_app(app) 
bcrypt.init_app(app)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


# O Render usará a variável de ambiente DATABASE_URL. Localmente, usaremos SQLite.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///db.sqlite3'
).replace('postgres://', 'postgresql://') # Necessário para compatibilidade com Render/Heroku

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()     
    app.run(host="0.0.0.0", port=5000, debug=True)