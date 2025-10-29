import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../static/images/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    if file and file.filename != '':
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}-{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            # Retorna o caminho e NULO para erro (Sucesso)
            return f"images/uploads/{unique_filename}", None
        else:
            # Retorna NULO para o caminho e a mensagem de erro (Falha de Validação)
            return None, "Extensão de arquivo não permitida. Use PNG, JPG, JPEG ou GIF."
    
    # Retorna NULO para o caminho e NULO para erro (Nenhum arquivo enviado, o que é opcional)
    return None, None