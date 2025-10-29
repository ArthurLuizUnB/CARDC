from models.database_config import Session # NOVO: Importa a Session pura
from models.ciclo_de_estudo import CicloDeEstudo
from sqlalchemy.orm.exc import NoResultFound

class CicloController:
    
    @staticmethod
    def listar_por_usuario(id_usuario):
        # NOVO: Consulta todos os ciclos de um usuário específico
        return Session.query(CicloDeEstudo).filter_by(id_usuario=id_usuario).all()

    @staticmethod
    def adicionar(novo_ciclo):
        # NOVO: Adiciona e salva a sessão
        Session.add(novo_ciclo)
        try:
            Session.commit()
            return True
        except Exception as e:
            Session.rollback()
            return False

    @staticmethod
    def buscar_por_id(ciclo_id):
        # NOVO: Busca o ciclo pela chave primária (equivalente ao get)
        return Session.get(CicloDeEstudo, ciclo_id)

    @staticmethod
    def atualizar(ciclo_atualizado):
        # NOVO: O SQLAlchemy puro detecta a mudança no objeto e faz o update no commit
        try:
            Session.commit()
            return True
        except Exception as e:
            Session.rollback()
            return False

    @staticmethod
    def remover(ciclo_id):
        ciclo = CicloController.buscar_por_id(ciclo_id)
        if ciclo:
            # NOVO: Remove e salva
            Session.delete(ciclo)
            try:
                Session.commit()
                return True
            except Exception as e:
                Session.rollback()
                return False
        return False