import uuid

class CicloDeEstudo:
    def __init__(self, id, id_usuario, obra, compositor, data_inicio, data_finalizacao,
                 link_gravacao="", consideracoes_preliminares="", acao_artistica="",
                 descricao_tarefa="", resultado_tecnico="", resultado_musical="",
                 observacoes="", pensamentos_associados="", emocoes_associadas="",
                 diario_reflexivo="", status="em_andamento", capa_url=""):
        self.id = id
        self.id_usuario = id_usuario
        self.obra = obra
        self.compositor = compositor
        self.data_inicio = data_inicio
        self.data_finalizacao = data_finalizacao
        self.link_gravacao = link_gravacao
        self.consideracoes_preliminares = consideracoes_preliminares
        self.acao_artistica = acao_artistica
        self.descricao_tarefa = descricao_tarefa
        self.resultado_tecnico = resultado_tecnico
        self.resultado_musical = resultado_musical
        self.observacoes = observacoes
        self.pensamentos_associados = pensamentos_associados
        self.emocoes_associadas = emocoes_associadas
        self.diario_reflexivo = diario_reflexivo
        self.status = status
        self.capa_url = capa_url

    def __repr__(self):
        return f"<CicloDeEstudo {self.id}: {self.obra}>"

    def to_dict(self):
        return self.__dict__