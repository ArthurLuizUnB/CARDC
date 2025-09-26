from flask import Flask
from routes.routes import routes
from datetime import datetime

app = Flask(__name__, template_folder="views/html")
app.secret_key = "music_app_secret_key_bmvc_2024"

# A linha de configuração foi movida para o arquivo principal
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)