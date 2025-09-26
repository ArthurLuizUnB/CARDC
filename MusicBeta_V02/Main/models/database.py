import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), '../data/db.json')

class Database:
    @staticmethod
    def load():
        if not os.path.exists(DB_FILE):
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            data = {
                "usuarios": [],
                "ciclos_de_estudo": []
            }
        else:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)

        # Garantir que as chaves existem, mesmo se o arquivo já existir mas estiver incompleto
        if "usuarios" not in data:
            data["usuarios"] = []
        if "ciclos_de_estudo" not in data:
            data["ciclos_de_estudo"] = []

        return data

    @staticmethod
    def save(data):
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)