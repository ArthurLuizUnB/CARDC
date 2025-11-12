# MusicBeta_V02/Main/controllers/gravacao_controller.py
from models.database_config import Session
from models.gravacao import Gravacao
from sqlalchemy.orm.exc import NoResultFound

class GravacaoController:
    
    @staticmethod
    def adicionar(nova_gravacao):
        """Adiciona uma nova gravação ao banco."""
        Session.add(nova_gravacao)
        try:
            Session.commit()
            return True
        except Exception as e:
            Session.rollback()
            print(f"Erro ao adicionar gravação: {e}")
            return False

    @staticmethod
    def listar_por_ciclo(id_ciclo):
        """Lista todas as gravações de um ciclo, ordenadas pela data de envio."""
        return Session.query(Gravacao).filter_by(id_ciclo=id_ciclo).order_by(Gravacao.data_envio.desc()).all()

    @staticmethod
    def remover(id_gravacao):
        """Remove uma gravação pelo seu ID."""
        gravacao = Session.get(Gravacao, id_gravacao)
        if gravacao:
            Session.delete(gravacao)
            try:
                Session.commit()
                return True
            except Exception as e:
                Session.rollback()
                return False
        return False