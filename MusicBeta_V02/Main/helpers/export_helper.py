import io
import re
import unicodedata
from datetime import datetime
from xml.sax.saxutils import escape

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

TEXTO_VAZIO = "Nenhum conteúdo registrado"


def _formatar_valor(valor):
    """Retorna o texto limpo ou a mensagem padrão caso o campo esteja vazio."""
    if valor is None:
        return TEXTO_VAZIO
    texto = str(valor).strip()
    return texto if texto else TEXTO_VAZIO


def _formatar_data(data_str):
    """Converte datas YYYY-MM-DD para DD/MM/YYYY quando possível."""
    if not data_str or not str(data_str).strip():
        return TEXTO_VAZIO
    texto = str(data_str).strip()
    try:
        dt = datetime.strptime(texto, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return texto


def obter_campos_ciclo(ciclo):
    """
    Retorna os metadados e os campos reflexivos na ordem oficial da metodologia CARDC.
    """
    metadados = [
        ("Obra", _formatar_valor(ciclo.obra)),
        ("Compositor", _formatar_valor(ciclo.compositor)),
        ("Data de Início", _formatar_data(ciclo.data_inicio)),
        ("Data de Finalização", _formatar_data(ciclo.data_finalizacao)),
    ]

    secoes = [
        ("Considerações Preliminares", _formatar_valor(ciclo.consideracoes_preliminares)),
        ("Ação Artística", _formatar_valor(ciclo.acao_artistica)),
        ("Descrição da Tarefa", _formatar_valor(ciclo.descricao_tarefa)),
        ("Resultado Técnico", _formatar_valor(ciclo.resultado_tecnico)),
        ("Resultado Musical", _formatar_valor(ciclo.resultado_musical)),
        ("Observações", _formatar_valor(ciclo.observacoes)),
        ("Pensamentos Associados", _formatar_valor(ciclo.pensamentos_associados)),
        ("Emoções Associadas", _formatar_valor(ciclo.emocoes_associadas)),
        ("Diário Reflexivo", _formatar_valor(ciclo.diario_reflexivo)),
    ]

    return metadados, secoes


def gerar_nome_arquivo(ciclo, extensao):
    """Gera um nome de arquivo seguro e legível a partir do nome da obra."""
    obra_base = ciclo.obra if ciclo and ciclo.obra else "ciclo"
    normalizado = unicodedata.normalize("NFKD", str(obra_base))
    sem_acentos = normalizado.encode("ascii", "ignore").decode("ascii")
    limpo = re.sub(r"[^a-zA-Z0-9_-]+", "_", sem_acentos).strip("_")
    if not limpo:
        limpo = "ciclo"
    return f"CARDC_{limpo[:50]}.{extensao.lstrip('.')}"


def gerar_txt(ciclo):
    """Gera o documento do ciclo em formato .txt (UTF-8) em memória."""
    metadados, secoes = obter_campos_ciclo(ciclo)
    linhas = [
        "=" * 65,
        "CICLO ARTÍSTICO-REFLEXIVO DE DUPLA CHECAGEM (CARDC)",
        "=" * 65,
        "",
    ]

    for rotulo, valor in metadados:
        linhas.append(f"{rotulo}: {valor}")

    linhas.append("")
    linhas.append("-" * 65)
    linhas.append("")

    for titulo, conteudo in secoes:
        linhas.append(f"[{titulo.upper()}]")
        linhas.append(conteudo)
        linhas.append("")

    linhas.append("=" * 65)
    texto_final = "\n".join(linhas)

    buffer = io.BytesIO()
    buffer.write(texto_final.encode("utf-8"))
    buffer.seek(0)
    return buffer


def gerar_pdf(ciclo):
    """Gera o documento do ciclo em formato .pdf em memória usando ReportLab."""
    metadados, secoes = obter_campos_ciclo(ciclo)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"CARDC - {ciclo.obra or 'Ciclo de Estudo'}",
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloCARDC",
        parent=estilos["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#FF9800"),
        spaceAfter=12,
    )

    estilo_meta = ParagraphStyle(
        "MetaCARDC",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#333333"),
        spaceAfter=4,
    )

    estilo_secao = ParagraphStyle(
        "SecaoCARDC",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#CC7A00"),
        spaceBefore=12,
        spaceAfter=4,
    )

    estilo_corpo = ParagraphStyle(
        "CorpoCARDC",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#222222"),
        spaceAfter=8,
    )

    elementos = []
    elementos.append(Paragraph("Ciclo Artístico-Reflexivo de Dupla Checagem (CARDC)", estilo_titulo))
    elementos.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#FF9800"), spaceAfter=12))

    for rotulo, valor in metadados:
        texto_meta = f"<b>{escape(rotulo)}:</b> {escape(valor)}"
        elementos.append(Paragraph(texto_meta, estilo_meta))

    elementos.append(Spacer(1, 8))
    elementos.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=8))

    for titulo, conteudo in secoes:
        elementos.append(Paragraph(escape(titulo), estilo_secao))
        conteudo_html = escape(conteudo).replace("\n", "<br/>")
        elementos.append(Paragraph(conteudo_html, estilo_corpo))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def gerar_docx(ciclo):
    """Gera o documento do ciclo em formato .docx em memória usando python-docx."""
    metadados, secoes = obter_campos_ciclo(ciclo)
    doc = Document()

    titulo_principal = doc.add_heading("Ciclo Artístico-Reflexivo de Dupla Checagem (CARDC)", level=1)
    titulo_principal.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in titulo_principal.runs:
        run.font.color.rgb = RGBColor(0xFF, 0x98, 0x00)

    for rotulo, valor in metadados:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        run_rotulo = p.add_run(f"{rotulo}: ")
        run_rotulo.bold = True
        p.add_run(valor)

    doc.add_paragraph()

    for titulo, conteudo in secoes:
        h = doc.add_heading(titulo, level=2)
        for run in h.runs:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(0xCC, 0x7A, 0x00)

        p = doc.add_paragraph(conteudo)
        p.paragraph_format.space_after = Pt(10)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
