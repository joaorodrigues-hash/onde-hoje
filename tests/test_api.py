import sys
import os

# Garante que o Python encontre os módulos dentro de backend/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pagina_inicial_deve_retornar_sucesso():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "A API do Onde Hoje está a rodar com sucesso!" in resposta.json()["mensagem"] or \
           "A API do Onde Hoje está rodando com sucesso!" in resposta.json()["mensagem"]

def test_listar_categorias_deve_retornar_lista_com_status_200():
    resposta = client.get("/categorias/")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

def test_explorar_roles_deve_retornar_lista_com_status_200():
    resposta = client.get("/roles/explorar")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

def test_adicionar_categoria_valida():
    nova_categoria = {"nome": "Teatro e Cultura"}
    resposta = client.post("/categorias/add", json=nova_categoria)
    # 200 se criou, ou 400 se já existia no banco
    assert resposta.status_code in [200, 400]