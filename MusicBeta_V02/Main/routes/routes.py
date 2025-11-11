from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from controllers.auth_controller import AuthController
from controllers.ciclo_controller import CicloController
from models.ciclo_de_estudo import CicloDeEstudo
from models.usuario import Usuario
import uuid
from datetime import datetime
from functools import wraps

routes = Blueprint("routes", __name__)

# routes/routes.py

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado():
            return redirect(url_for("routes.login"))
        
        g.usuario_atual = AuthController.usuario_atual()
        
        # CORREÇÃO CRÍTICA PARA SESSÃO ANTIGA (NOVA LÓGICA):
        if not g.usuario_atual or not hasattr(g.usuario_atual, 'id'):
            # Se o usuário logado (pela sessão) não puder ser encontrado no novo BD
            AuthController.fazer_logout()
            flash("Sessão expirada. Por favor, faça login novamente.", "info")
            return redirect(url_for("routes.login"))
            
        return f(*args, **kwargs)
    return decorated_function

@routes.route("/login", methods=["GET", "POST"])
def login():
    if AuthController.usuario_logado():
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        usuario, erro = AuthController.autenticar(username, password)
        if usuario:
            AuthController.fazer_login(usuario)
            flash(f"Bem-vindo, {usuario.username}!", "success")
            return redirect(url_for("routes.home"))
        else:
            flash(erro, "error")
            return render_template("login.html")

    return render_template("login.html")

@routes.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # NOVO: Coleta o nome completo do formulário
        nome_completo = request.form.get("nome_completo") 
        profile_pic_file = request.files.get("foto_perfil")

        if AuthController.buscar_por_username(username):
            flash("Nome de usuário já existe. Por favor, escolha outro.", "error")
            return render_template("cadastro.html")

        # Chama a função atualizada, passando o nome_completo
        novo_usuario, erro_foto = AuthController.adicionar_usuario(username, email, password, profile_pic_file, nome_completo=nome_completo)
        
        # Novo: Trata o erro de upload (Lógica da tarefa 1)
        if erro_foto:
            flash(erro_foto, "error")
            return render_template("cadastro.html")

        flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("routes.login"))

    return render_template("cadastro.html")

@routes.route("/logout")
def logout():
    AuthController.fazer_logout()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("routes.login"))

@routes.route("/")
@login_required
def home():
    # NOVO: Acessa o ID do usuário como atributo e filtra a lista de objetos
    ciclos = CicloController.listar_por_usuario(g.usuario_atual.id)
    ciclos_em_andamento = [c for c in ciclos if c.status == "em_andamento"]
    ciclos_finalizados = [c for c in ciclos if c.status == "finalizado"]
    return render_template("home.html", ciclos_em_andamento=ciclos_em_andamento, ciclos_finalizados=ciclos_finalizados)

@routes.route("/ciclo/novo", methods=["GET", "POST"])
@login_required
def novo_ciclo():
    if request.method == "POST":
        
        novo_ciclo = CicloDeEstudo(
            id=str(uuid.uuid4()),
            id_usuario=g.usuario_atual.id,
            obra=request.form.get("obra"),
            compositor=request.form.get("compositor"),
            data_inicio=request.form.get("data_inicio"),
            data_finalizacao=request.form.get("data_finalizacao"),
            link_gravacao=request.form.get("link_gravacao"),
            # O campo 'consideracoes_preliminares' existe no modelo mas não no form,
            # então ele será 'None' por padrão, o que está correto.
            acao_artistica=request.form.get("acao_artistica"),
            descricao_tarefa=request.form.get("descricao_tarefa"),
            resultado_tecnico=request.form.get("resultado_tecnico"),
            resultado_musical=request.form.get("resultado_musical"),
            observacoes=request.form.get("observacoes"),
            pensamentos_associados=request.form.get("pensamentos_associados"),
            emocoes_associadas=request.form.get("emocoes_associadas"),
            diario_reflexivo=request.form.get("diario_reflexivo"),
            status="finalizado" if request.form.get("terminado") else "em_andamento"
        )

        CicloController.adicionar(novo_ciclo)
        flash("Novo ciclo de estudo criado com sucesso!", "success")
        return redirect(url_for("routes.editar_ciclo", ciclo_id=novo_ciclo.id))

    return render_template("form_ciclo.html")

@routes.route("/ciclo/editar/<ciclo_id>", methods=["GET", "POST"])
@login_required
def editar_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    # NOVO: Acessa o ID do usuário como atributo
    if not ciclo or ciclo.id_usuario != g.usuario_atual.id:
        flash("Ciclo de estudo não encontrado ou você não tem permissão para editá-lo.", "error")
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        ciclo.obra = request.form.get("obra")
        ciclo.compositor = request.form.get("compositor")
        ciclo.data_inicio = request.form.get("data_inicio")
        ciclo.data_finalizacao = request.form.get("data_finalizacao")
        ciclo.link_gravacao = request.form.get("link_gravacao")
        ciclo.consideracoes_preliminares = request.form.get("consideracoes_preliminares")
        ciclo.acao_artistica = request.form.get("acao_artistica")
        ciclo.descricao_tarefa = request.form.get("descricao_tarefa")
        ciclo.resultado_tecnico = request.form.get("resultado_tecnico")
        ciclo.resultado_musical = request.form.get("resultado_musical")
        ciclo.observacoes = request.form.get("observacoes")
        ciclo.pensamentos_associados = request.form.get("pensamentos_associados")
        ciclo.emocoes_associadas = request.form.get("emocoes_associadas")
        ciclo.diario_reflexivo = request.form.get("diario_reflexivo")
        ciclo.status = "finalizado" if request.form.get("terminado") else "em_andamento"
        
        CicloController.atualizar(ciclo)
        flash("Ciclo de estudo atualizado com sucesso!", "success")
        return redirect(url_for("routes.home"))

    return render_template("form_ciclo.html", ciclo=ciclo)

@routes.route("/ciclo/finalizar/<ciclo_id>")
@login_required
def finalizar_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    # NOVO: Acessa o ID do usuário como atributo
    if ciclo and ciclo.id_usuario == g.usuario_atual.id:
        ciclo.status = "finalizado"
        CicloController.atualizar(ciclo)
        flash("Ciclo de estudo finalizado!", "success")
    return redirect(url_for("routes.home"))

@routes.route("/ciclo/remover/<ciclo_id>")
@login_required
def remover_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    # NOVO: Acessa o ID do usuário como atributo
    if ciclo and ciclo.id_usuario == g.usuario_atual.id:
        CicloController.remover(ciclo_id)
        flash("Ciclo de estudo removido com sucesso.", "success")
    return redirect(url_for("routes.home"))

@routes.route("/perfil")
@login_required
def perfil():
    # NOVO: Acessa o ID do usuário como atributo
    ciclos = CicloController.listar_por_usuario(g.usuario_atual.id)
    
    # NOVO: Filtra usando o atributo 'status' do objeto CicloDeEstudo
    incompletos = sum(1 for c in ciclos if c.status == "em_andamento")
    concluidos = sum(1 for c in ciclos if c.status == "finalizado")
    publicados = 0 
    
    # NOVO: g.usuario_atual já é o objeto completo do usuário
    usuario = g.usuario_atual
    
    return render_template("perfil.html",
                           usuario=usuario, 
                           incompletos=incompletos, 
                           concluidos=concluidos, 
                           publicados=publicados)

@routes.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    # NOVO: Acessa o ID do usuário como atributo
    usuario_id = g.usuario_atual.id
    # usuario = AuthController.buscar_por_id(usuario_id) # Não é mais necessário, já temos o objeto completo em g
    usuario = g.usuario_atual # Simplifica o código

    if request.method == "POST":
        profile_pic_file = request.files.get("foto_perfil")
        
        usuario.username = request.form.get("username")
        usuario.email = request.form.get("email")
        usuario.nome_completo = request.form.get("nome_completo")
        usuario.biografia = request.form.get("biografia")
        
        # Chama a função atualizada que retorna a mensagem de erro ou None em caso de sucesso
        erro_foto = AuthController.atualizar_usuario(usuario, profile_pic_file)
        
        # Novo: Trata o erro de upload
        if erro_foto:
            flash(erro_foto, "error")
            # Permanece na página de edição para o usuário corrigir
            return render_template("form_perfil.html", usuario=usuario)

        # Se o perfil foi atualizado com sucesso (erro_foto é None)
        session['username'] = usuario.username

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("routes.perfil"))

    return render_template("form_perfil.html", usuario=usuario)