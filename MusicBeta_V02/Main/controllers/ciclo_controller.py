from models.database_config import db # NOVO: Importa db
from models.ciclo_de_estudo import CicloDeEstudo
from flask import session # Mantido por precaução, mas não usado diretamente aqui

class CicloController:

    @staticmethod
    def listar_todos():
        # NOVO: Busca todos os ciclos
        return CicloDeEstudo.query.all()
    
    @staticmethod
    def buscar_por_id(ciclo_id):
        # NOVO: Busca o ciclo pela chave primária
        return CicloDeEstudo.query.get(ciclo_id)
    
    @staticmethod
    def listar_por_usuario(id_usuario):
        # NOVO: Filtra ciclos pelo id_usuario
        return CicloDeEstudo.query.filter_by(id_usuario=id_usuario).all()

    @staticmethod
    def adicionar(novo_ciclo):
        # NOVO: Adiciona e salva
        db.session.add(novo_ciclo)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # print(f"Erro ao adicionar ciclo: {e}") 
            return False

    @staticmethod
    def atualizar(ciclo_atualizado):
        # NOVO: O SQLAlchemy detecta a mudança no objeto e faz o update no commit
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # print(f"Erro ao atualizar ciclo: {e}") 
            return False
    
    @staticmethod
    def remover(ciclo_id):
        ciclo = CicloController.buscar_por_id(ciclo_id)
        if ciclo:
            # NOVO: Remove e salva
            db.session.delete(ciclo)
            try:
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                # print(f"Erro ao remover ciclo: {e}") 
                return False
        return False