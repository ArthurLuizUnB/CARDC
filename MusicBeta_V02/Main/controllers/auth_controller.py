from models.database_config import db 
from models.usuario import Usuario
from flask import session
import uuid
from helpers.upload_helper import save_profile_picture
from sqlalchemy import or_  # Adicionado para consultas ORM
from models.bcrypt_config import bcrypt

class AuthController:

    @staticmethod
    def listar_usuarios():
        # NOVO: Busca todos os usuários
        return Usuario.query.all()

    @staticmethod
    def buscar_por_username(username):
        # NOVO: Busca o primeiro usuário com o username correspondente
        return Usuario.query.filter_by(username=username).first()

    @staticmethod
    def buscar_por_id(id_usuario):
        # NOVO: Busca o usuário pela chave primária
        return Usuario.query.get(id_usuario)

    @staticmethod
    def validar_credenciais(username, password):
        # NOVO: Busca o usuário pelo username OU email
        usuario = Usuario.query.filter(
            or_(Usuario.username == username, Usuario.email == username)
        ).first()

        if usuario:
            if bcrypt.check_password_hash(usuario.password, password):
                return usuario, None
        
        return None, "Nome de usuário/email ou senha incorretos."
        
    @staticmethod
    def autenticar(username, password):
        return AuthController.validar_credenciais(username, password)

 @staticmethod
    def adicionar_usuario(username, email, password, profile_pic_file=None, nome_completo=None):
        id_usuario = str(uuid.uuid4())
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        caminho_foto_perfil = None
        erro_foto = None 

        if profile_pic_file and profile_pic_file.filename != '':
            caminho_foto_perfil, erro_foto = save_profile_picture(profile_pic_file)
            
            if erro_foto:
                return None, erro_foto 
        
        novo_usuario = Usuario(
            id=id_usuario,
            username=username,
            password=hashed_password,
            email=email,
            nome_completo=nome_completo or username,
            biografia="",
            is_admin=False,
            caminho_foto_perfil=caminho_foto_perfil
        )

        # NOVO: Adiciona o objeto à sessão e salva no banco de dados
        db.session.add(novo_usuario)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, "Erro ao salvar o novo usuário no banco de dados."
        
        return novo_usuario, None

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
            # NOVO: Retorna o objeto completo do usuário (que é a instância de Usuario)
            # Como a rota/template ainda espera um dict, estamos mantendo o to_dict() por enquanto.
            if usuario_completo:
                return usuario_completo
            return usuario_data
        return None

    @staticmethod
    def atualizar_usuario(usuario_atualizado, profile_pic_file=None):
        if profile_pic_file and profile_pic_file.filename != '':
            caminho_foto_perfil, erro_foto = save_profile_picture(profile_pic_file)
            
            if erro_foto:
                return erro_foto
            
            if caminho_foto_perfil:
                usuario_atualizado.caminho_foto_perfil = caminho_foto_perfil

        # NOVO: O SQLAlchemy detecta a mudança no objeto e faz o update no commit
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return "Erro ao atualizar o usuário no banco de dados."
        
        return None