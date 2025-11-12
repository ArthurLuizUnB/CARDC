# MusicBeta_V02/Main/tests/test_media_upload_helper.py
import pytest
from unittest.mock import MagicMock
from helpers import media_upload_helper

# Mock da classe FileStorage do Flask
class MockFile:
    def __init__(self, filename):
        self.filename = filename

def test_upload_image_success(mocker):
    """Testa se upload_image chama o uploader do Cloudinary corretamente."""
    
    # 1. Simula (mock) a função 'uploader.upload' do Cloudinary
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    # 2. Define o valor que a simulação deve retornar
    mock_upload.return_value = {"secure_url": "http://example.com/image.jpg"}
    
    mock_file = MockFile("test.jpg")
    url, erro = media_upload_helper.upload_image(mock_file)
    
    # 3. Verifica se a função foi chamada com os argumentos corretos
    mock_upload.assert_called_once_with(
        mock_file,
        folder="profile_pics",
        resource_type="image"
    )
    # 4. Verifica se o retorno está correto
    assert url == "http://example.com/image.jpg"
    assert erro is None

def test_upload_video_success(mocker):
    """Testa se upload_video chama o uploader com resource_type='video'."""
    
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    mock_upload.return_value = {"secure_url": "http://example.com/video.mp4"}
    
    mock_file = MockFile("test.mp4")
    url, erro = media_upload_helper.upload_video(mock_file)
    
    # Verifica o argumento CRÍTICO 'resource_type'
    mock_upload.assert_called_once_with(
        mock_file,
        folder="cycle_videos",
        resource_type="video"
    )
    assert url == "http://example.com/video.mp4"
    assert erro is None

def test_upload_image_no_file():
    """Testa se não fazer upload de arquivo não retorna erro."""
    url, erro = media_upload_helper.upload_image(None)
    assert url is None
    assert erro is None
    
    url, erro = media_upload_helper.upload_image(MockFile(filename=""))
    assert url is None
    assert erro is None

def test_upload_failure(mocker):
    """Testa se um erro do Cloudinary é capturado e reportado."""
    
    # Simula o Cloudinary levantando uma exceção
    mocker.patch(
        'cloudinary.uploader.upload', 
        side_effect=media_upload_helper.CloudinaryError("Erro de Teste")
    )
    
    mock_file = MockFile("test.jpg")
    url, erro = media_upload_helper.upload_image(mock_file)
    
    assert url is None
    assert "Erro de Teste" in erro