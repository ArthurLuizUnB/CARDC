from models.database import Database
from models.usuario import Usuario
from flask import session
import uuid
from helpers.upload_helper import save_profile_picture

class AuthController:

    @staticmethod
    def listar_usuarios():
        db = Database.load()
        return db.get("usuarios", [])

    @staticmethod
    def adicionar_usuario(username, email, password, profile_pic_file=None):
        id_usuario = str(uuid.uuid4())
        hashed_password = Usuario.hash_password(password)
        caminho_foto_perfil = None
        if profile_pic_file:
            caminho_foto_perfil = save_profile_picture(profile_pic_file)

        novo_usuario = Usuario(
            id=id_usuario,
            username=username,
            password=hashed_password,
            email=email,
            nome_completo=username,
            biografia="",
            is_admin=False,
            caminho_foto_perfil=caminho_foto_perfil
        )

        db = Database.load()
        if "usuarios" not in db:
            db["usuarios"] = []
        db["usuarios"].append(novo_usuario.to_dict())
        Database.save(db)
        return novo_usuario

    @staticmethod
    def buscar_por_username(username):
        if not username or not isinstance(username, str):
            return None

        username = username.strip().lower()

        usuarios = AuthController.listar_usuarios()
        for usuario_data in usuarios:
            if usuario_data["username"].lower() == username:
                return Usuario(**usuario_data)
        return None

    @staticmethod
    def buscar_por_id(id):
        if not id or not isinstance(id, str):
            return None

        usuarios = AuthController.listar_usuarios()
        for usuario_data in usuarios:
            if usuario_data["id"] == id:
                return Usuario(**usuario_data)
        return None

    @staticmethod
    def validar_credenciais(username, password):
        if not username or not password:
            return False, "Usuário e senha são obrigatórios"

        if len(username.strip()) < 3:
            return False, "Nome de usuário deve ter pelo menos 3 caracteres"

        if len(password) < 3:
            return False, "Senha deve ter pelo menos 3 caracteres"

        return True, ""

    @staticmethod
    def autenticar(username, password):
        valido, erro = AuthController.validar_credenciais(username, password)
        if not valido:
            return None, erro

        usuario = AuthController.buscar_por_username(username)
        if not usuario or not usuario.check_password(password):
            return None, "Usuário não encontrado"

        return usuario, None

    @staticmethod
    def fazer_login(usuario):
        session['user_id'] = usuario.id
        session['username'] = usuario.username
        session['is_admin'] = usuario.is_admin
        session['logged_in'] = True

    @staticmethod
    def fazer_logout():
        session.clear()

    @staticmethod
    def usuario_logado():
        return session.get('logged_in', False)

    @staticmethod
    def usuario_atual():
        if AuthController.usuario_logado():
            usuario_data = {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'is_admin': session.get('is_admin', False)
            }
            usuario_completo = AuthController.buscar_por_id(usuario_data['id'])
            if usuario_completo:
                return usuario_completo.to_dict()
            return usuario_data
        return None

    @staticmethod
    def atualizar_usuario(usuario_atualizado, profile_pic_file=None):
        if profile_pic_file:
            caminho_foto_perfil = save_profile_picture(profile_pic_file)
            if caminho_foto_perfil:
                usuario_atualizado.caminho_foto_perfil = caminho_foto_perfil

        db = Database.load()
        for i, u in enumerate(db["usuarios"]):
            if u["id"] == usuario_atualizado.id:
                db["usuarios"][i] = usuario_atualizado.to_dict()
                break
        Database.save(db)