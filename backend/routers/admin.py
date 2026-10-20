import os
import jwt
import sys
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from security import verificar_senha, gerar_hash_senha
from database import obter_conexao

router = APIRouter(prefix="/admin", tags=["Admin"])
SECRET_KEY = "mercos_chave_mestra_secreta"

class LoginAdmin(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login(dados: LoginAdmin):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, sobrenome, email, senha, cargo FROM admin WHERE email = ?", (dados.email,))
    row = cursor.fetchone()
    conn.close()

    if row and verificar_senha(dados.senha, row[4]):
        # Gera o Token de Segurança válido por 12 horas
        token = jwt.encode({"sub": row[3], "exp": datetime.utcnow() + timedelta(hours=12)}, SECRET_KEY, algorithm="HS256")
        return {"id": row[0], "nome": row[1], "sobrenome": row[2], "email": row[3], "cargo": row[5], "token": token}
    
    raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

@router.get("/stats")
def get_stats():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM roles WHERE status='aprovado'")
    aprovados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM roles WHERE status='pendente'")
    pendentes = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(likes), SUM(clicks_share) FROM roles")
    totais = cursor.fetchone()
    conn.close()
    
    total_likes = totais[0] if totais[0] else 0
    total_shares = totais[1] if totais[1] else 0
    
    return {
        "aprovados": aprovados, "pendentes": pendentes, "total_likes": total_likes, "total_shares": total_shares,
        "grafico": {"labels": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "curtidas": [120, 250, 310, total_likes], "compartilhamentos": [45, 90, 150, total_shares]}
    }

class NovoModerador(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str

@router.get("/moderadores")
def listar_moderadores():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, sobrenome, email, cargo FROM admin")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "nome": r[1], "sobrenome": r[2], "email": r[3], "cargo": r[4]} for r in rows]

@router.post("/moderadores")
def criar_moderador(dados: NovoModerador):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM admin WHERE email = ?", (dados.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    hash_senha = gerar_hash_senha(dados.senha)
    cursor.execute("INSERT INTO admin (nome, sobrenome, email, senha, cargo) VALUES (?, ?, ?, ?, ?)",
                   (dados.nome, dados.sobrenome, dados.email, hash_senha, "moderador"))
    conn.commit()
    conn.close()
    return {"status": "sucesso"}

@router.delete("/moderadores/{mod_id}")
def deletar_moderador(mod_id: int):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin WHERE id = ? AND cargo != 'master'", (mod_id,))
    conn.commit()
    conn.close()
    return {"status": "removido"}

class AtualizaPerfil(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha_antiga: str
    senha_nova: str = ""

@router.post("/perfil")
def atualizar_perfil(dados: AtualizaPerfil):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM admin WHERE email = ?", (dados.email,))
    row = cursor.fetchone()
    
    if not row or not verificar_senha(dados.senha_antiga, row[0]):
        conn.close()
        raise HTTPException(status_code=401, detail="Senha atual incorreta.")
        
    if dados.senha_nova:
        nova_hash = gerar_hash_senha(dados.senha_nova)
        cursor.execute("UPDATE admin SET nome=?, sobrenome=?, senha=? WHERE email=?", (dados.nome, dados.sobrenome, nova_hash, dados.email))
    else:
        cursor.execute("UPDATE admin SET nome=?, sobrenome=? WHERE email=?", (dados.nome, dados.sobrenome, dados.email))
    
    conn.commit()
    conn.close()
    return {"status": "atualizado"}