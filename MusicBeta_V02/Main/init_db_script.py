from app import app, init_db
import sys

# Executa a função de inicialização do BD
with app.app_context():
    init_db()