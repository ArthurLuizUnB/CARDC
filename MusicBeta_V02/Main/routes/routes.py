from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from controllers.auth_controller import AuthController
from controllers.ciclo_controller import CicloController
from models.ciclo_de_estudo import CicloDeEstudo
from models.usuario import Usuario
import uuid
from datetime import datetime
from functools import wraps

# Importações da Fase 3 (Corretas)
from helpers.media_upload_helper import upload_video 
from controllers.gravacao_controller import GravacaoController
from models.gravacao import Gravacao

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

# ==================================================================
# || As rotas /login, /cadastro, /logout, /
# || (Elas estão corretas, não precisam de mudança)
# ==================================================================

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

@routes.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if AuthController.usuario_logado():
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        email = request.form.get("email")
        enviado, mensagem = AuthController.solicitar_recuperacao_senha(email)
        
        if enviado:
            flash("Verifique seu e-mail para redefinir a senha.", "success")
            return redirect(url_for("routes.login"))
        else:
            # Exibe mensagem (mesmo que seja genérica para segurança)
            flash(mensagem, "info") 
            
    return render_template("esqueci_senha.html")

@routes.route("/resetar-senha/<token>", methods=["GET", "POST"])
def resetar_senha(token):
    if AuthController.usuario_logado():
        return redirect(url_for("routes.home"))

    # Verifica se o token é válido antes de mostrar o formulário
    email = AuthController.validar_token_recuperacao(token)
    if not email:
        flash("O link de recuperação é inválido ou expirou.", "error")
        return redirect(url_for("routes.esqueci_senha"))

    if request.method == "POST":
        nova_senha = request.form.get("password")
        sucesso, erro = AuthController.resetar_senha_por_token(token, nova_senha)
        
        if sucesso:
            flash("Sua senha foi atualizada! Faça login agora.", "success")
            return redirect(url_for("routes.login"))
        else:
            flash(erro, "error")

    return render_template("resetar_senha.html", token=token)    

@routes.route("/")
@login_required
def home():
    # NOVO: Acessa o ID do usuário como atributo e filtra a lista de objetos
    ciclos = CicloController.listar_por_usuario(g.usuario_atual.id)
    ciclos_em_andamento = [c for c in ciclos if c.status == "em_andamento"]
    ciclos_finalizados = [c for c in ciclos if c.status == "finalizado"]
    return render_template("home.html", ciclos_em_andamento=ciclos_em_andamento, ciclos_finalizados=ciclos_finalizados)

# ==================================================================
# || Rota /ciclo/novo
# || (O seu código estava 100% correto)
# ==================================================================

@routes.route("/ciclo/novo", methods=["GET", "POST"])
@login_required
def novo_ciclo():
    if request.method == "POST":
        
        # 1. Processa o upload do vídeo PRIMEIRO
        video_file = request.files.get("video_upload")
        video_url = None # Inicializa video_url aqui
        erro_video = None

        if video_file and video_file.filename != '':
            video_url, erro_video = upload_video(video_file)
            
            if erro_video:
                flash(f"Erro ao salvar o vídeo: {erro_video}", "error")
                return render_template("form_ciclo.html") 

        # 2. Cria o objeto CicloDeEstudo (SEM O LINK_GRAVACAO)
        novo_ciclo = CicloDeEstudo(
            id=str(uuid.uuid4()),
            id_usuario=g.usuario_atual.id,
            obra=request.form.get("obra"),
            compositor=request.form.get("compositor"),
            data_inicio=request.form.get("data_inicio"),
            data_finalizacao=request.form.get("data_finalizacao"),
            
            # REMOVIDO: link_gravacao=video_url, 
            
            consideracoes_preliminares=request.form.get("consideracoes_preliminares"), # Correção Bug 5
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

        # 3. Salva o NOVO CICLO primeiro
        CicloController.adicionar(novo_ciclo)

        # 4. Se um vídeo foi enviado, CRIE UMA NOVA GRAVACAO e ligue-a ao ciclo
        if video_url:
            nova_gravacao = Gravacao(
                id=str(uuid.uuid4()),
                id_ciclo=novo_ciclo.id, # Liga ao ciclo que acabamos de criar
                url_video=video_url,
                data_envio=datetime.utcnow()
            )
            GravacaoController.adicionar(nova_gravacao)
        
        flash("Novo ciclo de estudo criado com sucesso!", "success")
        return redirect(url_for("routes.editar_ciclo", ciclo_id=novo_ciclo.id))

    return render_template("form_ciclo.html", gravacoes=[], ciclo=None)

# ==================================================================
# || Rota /ciclo/editar/
# || (Aqui está a correção que faltava)
# ==================================================================

@routes.route("/ciclo/editar/<ciclo_id>", methods=["GET", "POST"])
@login_required
def editar_ciclo(ciclo_id):
    ciclo = CicloController.buscar_por_id(ciclo_id)
    if not ciclo or ciclo.id_usuario != g.usuario_atual.id:
        flash("Ciclo de estudo não encontrado...", "error")
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        
        # 1. Processa o upload de um NOVO vídeo (se um foi enviado)
        video_file = request.files.get("video_upload")
        if video_file and video_file.filename != '':
            video_url, erro_video = upload_video(video_file)
            
            if erro_video:
                flash(f"Erro ao salvar o vídeo: {erro_video}", "error")
                # Busca as gravações existentes para recarregar a página
                gravacoes = GravacaoController.listar_por_ciclo(ciclo_id)
                return render_template("form_ciclo.html", ciclo=ciclo, gravacoes=gravacoes)
            
            # Se o upload foi bem-sucedido, CRIE UMA NOVA GRAVACAO
            if video_url:
                nova_gravacao = Gravacao(
                    id=str(uuid.uuid4()),
                    id_ciclo=ciclo_id, # Liga ao ciclo atual
                    url_video=video_url,
                    data_envio=datetime.utcnow()
                )
                GravacaoController.adicionar(nova_gravacao)
        
        # 2. Atualiza os outros campos do ciclo
        ciclo.obra = request.form.get("obra")
        ciclo.compositor = request.form.get("compositor")
        ciclo.data_inicio = request.form.get("data_inicio")
        ciclo.data_finalizacao = request.form.get("data_finalizacao")
        ciclo.consideracoes_preliminares = request.form.get("consideracoes_preliminares") # Correção Bug 5
        ciclo.acao_artistica = request.form.get("acao_artistica")
        ciclo.descricao_tarefa = request.form.get("descricao_tarefa") # Linha que faltava no seu
        ciclo.resultado_tecnico = request.form.get("resultado_tecnico") # Linha que faltava no seu
        ciclo.resultado_musical = request.form.get("resultado_musical") # Linha que faltava no seu
        ciclo.observacoes = request.form.get("observacoes") # Linha que faltava no seu
        ciclo.pensamentos_associados = request.form.get("pensamentos_associados") # Linha que faltava no seu
        ciclo.emocoes_associadas = request.form.get("emocoes_associadas") # Linha que faltava no seu
        ciclo.diario_reflexivo = request.form.get("diario_reflexivo")
        ciclo.status = "finalizado" if request.form.get("terminado") else "em_andamento"
        
        CicloController.atualizar(ciclo)
        flash("Ciclo de estudo atualizado com sucesso!", "success")
        # Redireciona de volta para a EDIÇÃO para ver a nova lista de vídeos
        return redirect(url_for("routes.editar_ciclo", ciclo_id=ciclo_id))
    
    # Busca a lista de gravações para este ciclo
    gravacoes = GravacaoController.listar_por_ciclo(ciclo_id)
    # Passa a lista para o template
    return render_template("form_ciclo.html", ciclo=ciclo, gravacoes=gravacoes)

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

@routes.route("/gravacao/remover/<gravacao_id>")
@login_required
def remover_gravacao(gravacao_id):
    # 1. Busca a gravação no banco
    gravacao = GravacaoController.buscar_por_id(gravacao_id)
    
    # 2. Verifica se a gravação existe e se o utilizador logado é o "dono"
    # (Verificamos se o ID do utilizador no ciclo da gravação é o mesmo do utilizador logado)
    if not gravacao:
        flash("Gravação não encontrada.", "error")
        return redirect(url_for("routes.home"))

    # Guarda o ID do ciclo para onde vamos redirecionar
    id_ciclo = gravacao.id_ciclo 
    
    # Verificação de segurança (Lei 2)
    if gravacao.ciclo.id_usuario != g.usuario_atual.id:
        flash("Você não tem permissão para apagar esta gravação.", "error")
        return redirect(url_for("routes.editar_ciclo", ciclo_id=id_ciclo))

    # 3. Se tudo estiver certo, remove a gravação
    GravacaoController.remover(gravacao_id)
    flash("Gravação removida com sucesso!", "success")
    
    # 4. Redireciona de volta para a página de edição do ciclo
    return redirect(url_for("routes.editar_ciclo", ciclo_id=id_ciclo))    

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