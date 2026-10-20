import sys
import os
import pytest
from fastapi.testclient import TestClient

# Garante que os módulos da pasta backend sejam localizados corretamente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from main import app

client = TestClient(app)

def test_listar_categorias_com_sucesso():
    """Testa se a rota pública de categorias retorna status 200 e lista válida."""
    response = client.get("/categorias")
    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    if len(dados) > 0:
        assert "nome" in dados[0]

def test_explorar_eventos_publicos():
    """Testa se a rota de exploração de eventos futuros retorna status 200."""
    response = client.get("/roles/explorar")
    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)

def test_bloqueio_login_admin_invalido():
    """Testa se tentativa de login administrativo com senha incorreta é barrada (401)."""
    payload_invalido = {
        "email": "hacker@invasao.com",
        "senha": "senha_totalmente_errada"
    }
    response = client.post("/admin/login", json=payload_invalido)
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos."

def test_bloqueio_rota_protegida_sem_token():
    """Testa se o middleware JWT bloqueia requisições sem o cabeçalho Authorization."""
    response = client.get("/admin/stats")
    assert response.status_code == 401
    assert "Acesso negado" in response.json()["detail"]