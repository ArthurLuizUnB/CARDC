import hashlib

class Usuario:
    def __init__(self, id, username, password, email, nome_completo, biografia="", is_admin=False, caminho_foto_perfil=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.nome_completo = nome_completo
        self.biografia = biografia
        self.is_admin = is_admin
        self.caminho_foto_perfil = caminho_foto_perfil

    def __repr__(self):
        return f"<Usuario {self.id}: {self.username}>"

    def to_dict(self):
        return self.__dict__
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password == self.hash_password(password)