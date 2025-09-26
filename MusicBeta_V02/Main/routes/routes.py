from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from controllers.auth_controller import AuthController
from controllers.ciclo_controller import CicloController
from models.ciclo_de_estudo import CicloDeEstudo
from models.usuario import Usuario
import uuid
from datetime import datetime
from functools import wraps

routes = Blueprint("routes", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthController.usuario_logado():
            return redirect(url_for("routes.login"))
        g.usuario_atual = AuthController.usuario_atual()
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
        profile_pic_file = request.files.get("foto_perfil")

        if AuthController.buscar_por_username(username):
            flash("Nome de usuário já existe. Por favor, escolha outro.", "error")
            return render_template("cadastro.html")

        AuthController.adicionar_usuario(username, email, password, profile_pic_file)
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
    ciclos = CicloController.listar_por_usuario(g.usuario_atual["id"])
    ciclos_em_andamento = [c for c in ciclos if c.get("status") == "em_andamento"]
    ciclos_finalizados = [c for c in ciclos if c.get("status") == "finalizado"]
    return render_template("home.html", ciclos_em_andamento=ciclos_em_andamento, ciclos_finalizados=ciclos_finalizados)

@routes.route("/ciclo/novo", methods=["GET", "POST"])
@login_required
def novo_ciclo():
    if request.method == "POST":
        obra = request.form.get("obra")
        compositor = request.form.get("compositor")
        data_inicio = request.form.get("data_inicio")
        data_finalizacao = request.form.get("data_finalizacao")

        novo_ciclo = CicloDeEstudo(
            id=str(uuid.uuid4()),
            id_usuario=g.usuario_atual["id"],
            obra=obra,
            compositor=compositor,
            data_inicio=data_inicio,
            data_finalizacao=data_finalizacao
        )
        CicloController.adicionar(novo_ciclo)
        flash("Novo ciclo de estudo criado com sucesso!", "success")
        return redirect(url_for("routes.editar_ciclo", ciclo_id=novo_ciclo.id))

    return render_template("form_ciclo.html")

@routes.route("/ciclo/editar/<ciclo_id>", methods=["GET", "POST"])
@login_required
def editar_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    if not ciclo or ciclo.id_usuario != g.usuario_atual["id"]:
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
    if ciclo and ciclo.id_usuario == g.usuario_atual["id"]:
        ciclo.status = "finalizado"
        CicloController.atualizar(ciclo)
        flash("Ciclo de estudo finalizado!", "success")
    return redirect(url_for("routes.home"))

@routes.route("/ciclo/remover/<ciclo_id>")
@login_required
def remover_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    if ciclo and ciclo.id_usuario == g.usuario_atual["id"]:
        CicloController.remover(ciclo_id)
        flash("Ciclo de estudo removido com sucesso.", "success")
    return redirect(url_for("routes.home"))

@routes.route("/perfil")
@login_required
def perfil():
    ciclos = CicloController.listar_por_usuario(g.usuario_atual["id"])
    incompletos = sum(1 for c in ciclos if c.get("status") == "em_andamento")
    concluidos = sum(1 for c in ciclos if c.get("status") == "finalizado")
    publicados = 0 
    
    usuario = AuthController.buscar_por_id(g.usuario_atual["id"])
    
    return render_template("perfil.html",
                           usuario=usuario, 
                           incompletos=incompletos, 
                           concluidos=concluidos, 
                           publicados=publicados)

@routes.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    usuario_id = g.usuario_atual["id"]
    usuario = AuthController.buscar_por_id(usuario_id)

    if request.method == "POST":
        profile_pic_file = request.files.get("foto_perfil")
        
        usuario.username = request.form.get("username")
        usuario.email = request.form.get("email")
        usuario.nome_completo = request.form.get("nome_completo")
        usuario.biografia = request.form.get("biografia")
        
        AuthController.atualizar_usuario(usuario, profile_pic_file)
        
        session['username'] = usuario.username

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("routes.perfil"))

    return render_template("form_perfil.html", usuario=usuario)