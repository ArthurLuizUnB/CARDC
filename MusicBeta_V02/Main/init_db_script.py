from app import app, init_db
import sys

# Executa a função de inicialização do BD
try:
    with app.app_context():
        init_db()
except Exception as e:
    print(f"ERRO CRÍTICO NA INICIALIZAÇÃO DO BANCO: {e}")
    sys.exit(1)