# MusicBeta_V02/Main/tests/test_export_helper.py
from docx import Document
from models.ciclo_de_estudo import CicloDeEstudo
from helpers.export_helper import (
    TEXTO_VAZIO,
    obter_campos_ciclo,
    gerar_nome_arquivo,
    gerar_txt,
    gerar_pdf,
    gerar_docx,
)


def _criar_ciclo_exemplo():
    return CicloDeEstudo(
        id="ciclo-123",
        id_usuario="user-123",
        obra="Prelúdio nº 4",
        compositor="Heitor Villa-Lobos",
        data_inicio="2026-11-05",
        data_finalizacao=None,
        consideracoes_preliminares="Estudo de sonoridade no registro grave.",
        acao_artistica="",
        descricao_tarefa="   ",
        resultado_tecnico="Melhora na estabilidade da mão direita.",
        resultado_musical=None,
        observacoes=None,
        pensamentos_associados=None,
        emocoes_associadas="Concentração e calma.",
        diario_reflexivo="Sessão produtiva.\nPróximo passo: trabalhar seção B.",
    )


def test_obter_campos_ciclo_preenche_campos_vazios():
    """Verifica se campos vazios ou None recebem o texto padrão e datas são formatadas."""
    ciclo = _criar_ciclo_exemplo()
    metadados, secoes = obter_campos_ciclo(ciclo)

    dict_meta = dict(metadados)
    dict_secoes = dict(secoes)

    assert dict_meta["Obra"] == "Prelúdio nº 4"
    assert dict_meta["Compositor"] == "Heitor Villa-Lobos"
    assert dict_meta["Data de Início"] == "05/11/2026"
    assert dict_meta["Data de Finalização"] == TEXTO_VAZIO

    assert dict_secoes["Considerações Preliminares"] == "Estudo de sonoridade no registro grave."
    assert dict_secoes["Ação Artística"] == TEXTO_VAZIO
    assert dict_secoes["Descrição da Tarefa"] == TEXTO_VAZIO
    assert dict_secoes["Resultado Musical"] == TEXTO_VAZIO
    assert dict_secoes["Emoções Associadas"] == "Concentração e calma."


def test_gerar_nome_arquivo_higieniza_acentos_e_simbolos():
    """Garante que o nome do arquivo seja seguro para qualquer sistema operacional."""
    ciclo = _criar_ciclo_exemplo()
    nome_pdf = gerar_nome_arquivo(ciclo, "pdf")
    assert nome_pdf == "CARDC_Preludio_no_4.pdf"


def test_gerar_txt_retorna_conteudo_completo_utf8():
    """Testa se o arquivo .txt gerado em memória contém todos os campos e textos esperados."""
    ciclo = _criar_ciclo_exemplo()
    buffer = gerar_txt(ciclo)
    conteudo = buffer.read().decode("utf-8")

    assert "CICLO ARTÍSTICO-REFLEXIVO DE DUPLA CHECAGEM (CARDC)" in conteudo
    assert "Obra: Prelúdio nº 4" in conteudo
    assert "Compositor: Heitor Villa-Lobos" in conteudo
    assert "05/11/2026" in conteudo
    assert TEXTO_VAZIO in conteudo
    assert "Sessão produtiva." in conteudo


def test_gerar_pdf_retorna_binario_pdf_valido():
    """Testa se o gerador de PDF produz um fluxo binário com cabeçalho PDF válido."""
    ciclo = _criar_ciclo_exemplo()
    buffer = gerar_pdf(ciclo)
    dados = buffer.read()

    assert dados.startswith(b"%PDF-")
    assert len(dados) > 500


def test_gerar_docx_retorna_documento_word_legivel():
    """Testa se o arquivo .docx gerado em memória pode ser aberto e contém os textos do ciclo."""
    ciclo = _criar_ciclo_exemplo()
    buffer = gerar_docx(ciclo)

    doc = Document(buffer)
    texto_completo = "\n".join(p.text for p in doc.paragraphs)

    assert "Prelúdio nº 4" in texto_completo
    assert "Heitor Villa-Lobos" in texto_completo
    assert TEXTO_VAZIO in texto_completo
    assert "Estudo de sonoridade no registro grave." in texto_completo
