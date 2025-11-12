# MusicBeta_V02/Main/helpers/media_upload_helper.py
import os
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

# 1. Configura o Cloudinary com as variáveis de ambiente que você definiu no Render
try:
    cloudinary.config(
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
        secure=True,
    )
except Exception as e:
    # Isso é útil para debug caso as variáveis de ambiente não sejam carregadas
    print(f"Erro ao configurar o Cloudinary: {e}")


def upload_image(file_to_upload):
    """
    Faz upload de uma IMAGEM (foto de perfil) para o Cloudinary.
    Retorna (secure_url, None) em sucesso, ou (None, error_message) em falha.
    """
    if not file_to_upload or file_to_upload.filename == '':
        return None, None # Nenhum arquivo, sem erro

    try:
        # Faz o upload para o Cloudinary, colocando na pasta 'profile_pics'
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            folder="profile_pics",
            resource_type="image" # Define que é uma imagem
        )
        
        # Retorna a URL segura e None (para erro)
        return upload_result.get("secure_url"), None

    except CloudinaryError as e:
        return None, f"Erro no upload da imagem: {str(e)}"
    except Exception as e:
        return None, f"Erro inesperado no upload: {str(e)}"


def upload_video(file_to_upload):
    """
    Faz upload de um VÍDEO (gravação do ciclo) para o Cloudinary.
    Retorna (secure_url, None) em sucesso, ou (None, error_message) em falha.
    """
    if not file_to_upload or file_to_upload.filename == '':
        return None, None # Nenhum arquivo, sem erro

    try:
        # Faz o upload, definindo resource_type="video"
        # Isso permite que o Cloudinary processe o vídeo corretamente
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            folder="cycle_videos",
            resource_type="video" # IMPORTANTE: Define que é um vídeo
        )
        
        # Retorna a URL segura e None (para erro)
        return upload_result.get("secure_url"), None

    except CloudinaryError as e:
        return None, f"Erro no upload do vídeo: {str(e)}"
    except Exception as e:
        return None, f"Erro inesperado no upload: {str(e)}"