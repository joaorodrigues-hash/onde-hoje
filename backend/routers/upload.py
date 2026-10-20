from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from uuid import uuid4

router = APIRouter(prefix="/upload", tags=["Uploads"])

# Pega o caminho absoluto da pasta backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

@router.post("/")
async def fazer_upload(file: UploadFile = File(...)):
    try:
        # Pega a extensão original do arquivo (ex: .jpg, .png)
        extensao = file.filename.split(".")[-1]
        # Gera um nome único e criptografado para evitar arquivos com mesmo nome
        nome_unico = f"{uuid4().hex}.{extensao}"
        caminho_completo = os.path.join(UPLOAD_DIR, nome_unico)
        
        # Salva o arquivo fisicamente na pasta uploads
        with open(caminho_completo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Retorna a URL pública para o frontend e para o banco de dados
        return {"url": f"http://127.0.0.1:8000/uploads/{nome_unico}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao salvar a imagem no servidor.")