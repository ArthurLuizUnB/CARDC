from models.database_config import Session 
from models.usuario import Usuario
from flask import session
import uuid
from helpers.media_upload_helper import upload_image # Sua nova importação (Correto)
from sqlalchemy import or_ 
from models.bcrypt_config import bcrypt 

class AuthController:

    @staticmethod
    def listar_usuarios():
        # NOVO: Consulta com Session.query(Modelo).all()
        return Session.query(Usuario).all()

    @staticmethod
    def buscar_por_username(username):
        # NOVO: Consulta com Session.query
        return Session.query(Usuario).filter_by(username=username).first()

    @staticmethod
    def buscar_por_id(id_usuario):
        # NOVO: Consulta com Session.get()
        return Session.get(Usuario, id_usuario)

    @staticmethod
    def validar_credenciais(username, password):
        # NOVO: Busca o usuário pelo username OU email usando Session
        usuario = Session.query(Usuario).filter(
            or_(Usuario.username == username, Usuario.email == username)
        ).first()

        if usuario:
            # Verifica a senha usando Bcrypt
            if bcrypt.check_password_hash(usuario.password, password):
                return usuario, None
        
        return None, "Nome de usuário/email ou senha incorretos."

    @staticmethod
    def autenticar(username, password):
        # NOTA: O método autenticar deve chamar validar_credenciais para mensagens de erro mais detalhadas
        valido, erro = AuthController.validar_credenciais(username, password)
        if not valido:
            return None, erro

        # NOVO: Busca o usuário pelo username OU email usando Session
        usuario = Session.query(Usuario).filter(
            or_(Usuario.username == username, Usuario.email == username)
        ).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            return usuario, None

        return None, "Nome de usuário/email ou senha incorretos."

@staticmethod
    def adicionar_usuario(username, email, password, profile_pic_file=None, nome_completo=None):
        id_usuario = str(uuid.uuid4())
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        caminho_foto_perfil = None
        erro_foto = None 

        if profile_pic_file and profile_pic_file.filename != '':
            # MUDANÇA: Usar o novo helper que envia para o Cloudinary
            caminho_foto_perfil, erro_foto = upload_image(profile_pic_file)
            
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
            caminho_foto_perfil=caminho_foto_perfil # Salva a URL do Cloudinary
        )

        Session.add(novo_usuario)
        try:
            Session.commit()
        except Exception as e:
            Session.rollback()
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
            usuario_id = session.get('user_id')
            # NOVO: Consulta o objeto completo
            usuario_completo = AuthController.buscar_por_id(usuario_id)
            
            # Não é mais necessário retornar um dicionário, retorna o objeto puro
            if usuario_completo:
                return usuario_completo
            
            # Fallback (não deve ser necessário se o login foi bem-sucedido)
            return {
                'id': usuario_id,
                'username': session.get('username'),
                'is_admin': session.get('is_admin', False)
            }
        return None

    @staticmethod
    def atualizar_usuario(usuario_atualizado, profile_pic_file=None):
        if profile_pic_file and profile_pic_file.filename != '':
            # MUDANÇA: Usar o novo helper que envia para o Cloudinary
            caminho_foto_perfil, erro_foto = upload_image(profile_pic_file)
            
            if erro_foto:
                return erro_foto
            
            if caminho_foto_perfil:
                usuario_atualizado.caminho_foto_perfil = caminho_foto_perfil # Salva a URL do Cloudinary

        try:
            Session.commit()
        except Exception as e:
            Session.rollback()
            return "Erro ao atualizar o usuário no banco de dados."
        
        return None