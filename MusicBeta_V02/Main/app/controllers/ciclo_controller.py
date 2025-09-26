from models.database import Database
from models.ciclo_de_estudo import CicloDeEstudo

class CicloController:
    @staticmethod
    def listar_por_usuario(id_usuario):
        db = Database.load()
        ciclos = db.get("ciclos_de_estudo", [])
        return [c for c in ciclos if c.get("id_usuario") == id_usuario]

    @staticmethod
    def adicionar(ciclo):
        db = Database.load()
        db["ciclos_de_estudo"].append(ciclo.to_dict())
        Database.save(db)

    @staticmethod
    def buscar_por_id(ciclo_id):
        db = Database.load()
        ciclos = db.get("ciclos_de_estudo", [])
        ciclo = next((c for c in ciclos if c.get("id") == ciclo_id), None)
        if ciclo:
            return CicloDeEstudo(**ciclo)
        return None

    @staticmethod
    def atualizar(ciclo_atualizado):
        db = Database.load()
        for i, c in enumerate(db["ciclos_de_estudo"]):
            if c["id"] == ciclo_atualizado.id:
                db["ciclos_de_estudo"][i] = ciclo_atualizado.to_dict()
                break
        Database.save(db)

    @staticmethod
    def remover(ciclo_id):
        db = Database.load()
        db["ciclos_de_estudo"] = [c for c in db["ciclos_de_estudo"] if c["id"] != ciclo_id]
        Database.save(db)