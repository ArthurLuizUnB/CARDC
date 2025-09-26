from flask import Flask
from routes.routes import routes
from datetime import datetime
import os # Importe a biblioteca os

app = Flask(__name__, template_folder="views/html")
# A linha abaixo foi alterada
app.secret_key = os.environ.get("SECRET_KEY", "uma_chave_padrao_para_desenvolvimento")

# O resto do seu código continua igual...
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)